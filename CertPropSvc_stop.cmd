echo off
cls

echo.
echo.
echo Stoping CertPropSvc (Certification Propagation Service): 

sc stop CertPropSvc
sc config CertPropSvc start=disabled

echo CertPropSvc (Certification Propagation Service) has been stopped successfully!
pause