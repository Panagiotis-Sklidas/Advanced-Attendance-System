echo off
cls

echo.
echo.
echo Stopping CertPropSvc (Certification Propagation Service): 

sc config CertPropSvc start=disabled
sc stop CertPropSvc

echo CertPropSvc (Certification Propagation Service) has been stopped successfully!
pause