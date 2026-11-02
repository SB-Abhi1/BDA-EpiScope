"""Shared paths, reproducibility, Spark session and audit utilities."""
from pathlib import Path
import os,json,hashlib,time
ROOT=Path(__file__).resolve().parent
DATA=Path(os.environ.get('EPISCOPE_DATA',str(ROOT/'data'))).resolve()
DISEASES=['dengue','diarrhoea','ili','malaria']
CODES={'A90':'dengue','A91':'dengue','A00':'diarrhoea','A09':'diarrhoea','J10':'ili','J11':'ili','B50':'malaria','B51':'malaria','B52':'malaria','B53':'malaria','B54':'malaria'}
def save(path,obj):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(obj,indent=2,default=str,allow_nan=False));tmp.replace(path)
def digest(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def spark(name='EpiScope',optimized=True):
 os.environ.setdefault('SPARK_LOCAL_IP','127.0.0.1')
 from pyspark.sql import SparkSession
 (DATA/'spark-events').mkdir(parents=True,exist_ok=True)
 s=(SparkSession.builder.master(os.environ.get('SPARK_MASTER','local[2]')).appName(name)
 .config('spark.driver.host','127.0.0.1').config('spark.driver.bindAddress','127.0.0.1')
 .config('spark.driver.memory',os.environ.get('SPARK_DRIVER_MEMORY','3g'))
 .config('spark.sql.shuffle.partitions','16').config('spark.sql.session.timeZone','UTC')
 .config('spark.sql.adaptive.enabled',str(optimized).lower())
 .config('spark.sql.autoBroadcastJoinThreshold','10485760' if optimized else '-1')
 .config('spark.eventLog.enabled','true').config('spark.eventLog.dir',str(DATA/'spark-events'))
 .config('spark.sql.warehouse.dir',str(DATA/'warehouse'))
 .config('javax.jdo.option.ConnectionURL','jdbc:derby:;databaseName='+str(DATA/'metastore_db')+';create=true').enableHiveSupport().getOrCreate())
 s.sparkContext.setLogLevel('ERROR');return s

def read_gold(session,name):
 """Select the latest completed logical Parquet snapshot, including legacy-file migrations."""
 from pyspark.sql import functions as F
 df=session.read.option('mergeSchema','true').parquet(str(DATA/'gold'/name))
 if 'snapshot_id' in df.columns:
  latest=df.agg(F.max('snapshot_id')).first()[0]
  if latest is not None:df=df.where(F.col('snapshot_id')==latest)
  df=df.drop('snapshot_id')
 return df

def read_current_pandas(path):
 """Compact final aggregate tables only; merge old/new schemas and select latest snapshot."""
 import pandas as pd
 frames=[]
 for p in Path(path).rglob('*.parquet'):
  if any(x.startswith(('_','.')) for x in p.relative_to(path).parts):continue
  f=pd.read_parquet(p)
  for part in p.relative_to(path).parts[:-1]:
   if '=' in part:
    k,v=part.split('=',1)
    if k not in f:f[k]=v
  frames.append(f)
 if not frames:
  raise FileNotFoundError(f'No Parquet output found at {path}. Complete analytics.run before serving.export.')
 result=pd.concat(frames,ignore_index=True)
 if 'snapshot_id' in result:
  latest=result.snapshot_id.max()
  if pd.notna(latest):result=result[result.snapshot_id==latest]
  result=result.drop(columns='snapshot_id')
 return result
