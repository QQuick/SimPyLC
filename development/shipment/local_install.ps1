$destination = "D:\python36_anaconda\Lib\site-packages\SimPyLC"
Remove-Item $destination -recurse
Copy-Item ..\..\SimPyLC $destination -recurse