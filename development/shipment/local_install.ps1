$destination = "D:\python37\Lib\site-packages\SimPyLC"
Remove-Item $destination -recurse
Copy-Item ..\..\SimPyLC $destination -recurse