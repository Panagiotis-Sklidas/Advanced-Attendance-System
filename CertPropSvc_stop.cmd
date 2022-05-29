echo off
cls

echo.
echo.
echo Stopping CertPropSvc (Certificate Propagation Service): 

sc config CertPropSvc start=disabled
sc stop CertPropSvc

echo CertPropSvc (Certificate Propagation Service) has been stopped successfully!
pause