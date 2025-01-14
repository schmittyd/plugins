$VERSION = "4.9.4"
$URL = "https://get.filebot.net/filebot/FileBot_${VERSION}/FileBot_${VERSION}"

wingetcreate update --id PointPlanck.FileBot --version $VERSION --url "${URL}_x64.msi" "${URL}_x86.msi"

winget validate --manifest "manifests\p\PointPlanck\FileBot\${VERSION}"
