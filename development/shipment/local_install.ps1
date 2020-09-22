$destination = "D:\python37\Lib\site-packages\simpylc"
Remove-Item $destination -recurse
Copy-Item ..\..\simpylc $destination -recurse
