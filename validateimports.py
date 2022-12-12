# from msspackages import bucketization
# bucketization.bucko("good job")




# from msspackages.bucketization import bucko
# bucko("bad job")

from msspackages import Circle
from msspackages import Pyspark_data_ingestion
from msspackages import setup_runner
from msspackages import get_features

# ci = Circle(5,"red")

# #ci.describe(ci)

# setup_runner('notebook')

# df_build = Pyspark_data_ingestion(year = '2022', month = '5', day = '5', hour = '5', filter_column_value = 'Cluster')
# spark = df_build.get_spark()
# df_err, df =  df_build.read()
# if df_err == 'PASS':
#     df.show()

print(get_features())
