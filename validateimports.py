# from msspackages import bucketization
# bucketization.bucko("good job")




# from msspackages.bucketization import bucko
# bucko("bad job")

from msspackages import Circle
from msspackages import Pyspark_data_ingestion

ci = Circle(5,"red")

#ci.describe(ci)

df = Pyspark_data_ingestion(year = '2022', month = '5', day = '5', hour = '5', filter_column_value = 'Cluster')
df.show()