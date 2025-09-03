from analytics.io.reader import reader_data
from analytics.io.writer import writer_data
from analytics.core.processor import processor_data
from analytics.tools.formatter import formatter_data

data=reader_data()
data1=processor_data(data)
data2=formatter_data(data1)
print(writer_data(data2))