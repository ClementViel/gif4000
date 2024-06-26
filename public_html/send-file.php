<?php
// Attachment file
$file0 = "images/gif0.gif";
$file1 = "images/gif1.gif";
$file2 = "images/gif2.gif";
$files = array($file0, $file1, $file2);
$zipname = 'gifs.zip';
$zip = new ZipArchive;
$zip->open($zipname, ZipArchive::CREATE);
foreach ($files as $file) {
  $zip->addFile($file);
}
$zip->close();
// Preparing attachment
if (!empty($zipname) > 0)
{
    if (is_file($zipname))
    {
        header('Content-type: application/octet-stream');
        header("Content-Type: ".mime_content_type($zipname));
        header('Content-disposition: attachment; filename=gifs');
        while (ob_get_level()) {
           ob_end_clean();
        }
        readfile($zipname);
    }
}


?>

