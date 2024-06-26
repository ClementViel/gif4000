<?php
// recipient email address
$to = $_POST['to'];

// subject of the email
$subject = $_POST['subject'];

// message body
$message = $_POST['message'];


 

// Email subject
$subject = 'Voici votre GIF';

// Attachment file
$file0 = "images/gif0.gif";
$file1 = "images/gif1.gif";
$file2 = "images/gif2.gif";

// Email body content
$htmlContent = ' 
    <h3>Merci de votre participation !</h3> 
';

// Header for sender info
$headers = "From: gif4000" . " <" . "gif4000" . ">";

// Boundary
$semi_rand = md5(time());
$mime_boundary = "==Multipart_Boundary_x{$semi_rand}x";

// Headers for attachment
$headers .= "\nMIME-Version: 1.0\n" . "Content-Type: multipart/mixed;\n" . " boundary=\"{$mime_boundary}\"";

// Multipart boundary
$message0 = "--{$mime_boundary}\n" . "Content-Type: text/html; charset=\"UTF-8\"\n" . "Content-Transfer-Encoding: 7bit\n\n" . $htmlContent . "\n\n";

// Preparing attachment
if (!empty($file0) > 0)
{
    if (is_file($file0))
    {
        $message0 .= "--{$mime_boundary}\n";
        $fp = fopen($file0, "rb");
        $data = fread($fp, filesize($file0));

        fclose($fp);
        $data = chunk_split(base64_encode($data));
        $message0 .= "Content-Type: application/octet-stream; name=\"" . basename($file0) . "\"\n" . "Content-Description: " . basename($file0) . "\n" . "Content-Disposition: attachment;\n" . " filename=\"" . basename($file0) . "\"; size=" . filesize($file0) . ";\n" . "Content-Transfer-Encoding: base64\n\n" . $data . "\n\n";
    }
}

$message1 = "--{$mime_boundary}\n" . "Content-Type: text/html; charset=\"UTF-8\"\n" . "Content-Transfer-Encoding: 7bit\n\n" . $htmlContent . "\n\n";

// Preparing attachment
if (!empty($file1) > 0)
{
    if (is_file($file1))
    {
        $message1 .= "--{$mime_boundary}\n";
        $fp = fopen($file1, "rb");
        $data = fread($fp, filesize($file1));

        fclose($fp);
        $data = chunk_split(base64_encode($data));
        $message1 .= "Content-Type: application/octet-stream; name=\"" . basename($file1) . "\"\n" . "Content-Description: " . basename($file1) . "\n" . "Content-Disposition: attachment;\n" . " filename=\"" . basename($file0) . "\"; size=" . filesize($file0) . ";\n" . "Content-Transfer-Encoding: base64\n\n" . $data . "\n\n";
    }
}

$message2 = "--{$mime_boundary}\n" . "Content-Type: text/html; charset=\"UTF-8\"\n" . "Content-Transfer-Encoding: 7bit\n\n" . $htmlContent . "\n\n";

// Preparing attachment
if (!empty($file2) > 0)
{
    if (is_file($file2))
    {
        $message2 .= "--{$mime_boundary}\n";
        $fp = fopen($file2, "rb");
        $data = fread($fp, filesize($file2));

        fclose($fp);
        $data = chunk_split(base64_encode($data));
        $message2 .= "Content-Type: application/octet-stream; name=\"" . basename($file2) . "\"\n" . "Content-Description: " . basename($file2) . "\n" . "Content-Disposition: attachment;\n" . " filename=\"" . basename($file0) . "\"; size=" . filesize($file0) . ";\n" . "Content-Transfer-Encoding: base64\n\n" . $data . "\n\n";
    }
}

echo "sending email 0";
// send email
if (mail($to, $subject, $message0, $headers)) {
    echo "Email with attachment sent successfully.";
} else {
    echo "Failed to send email with attachment.";
}

echo "sending email 1";
// send email
if (mail($to, $subject, $message1, $headers)) {
    echo "Email with attachment sent successfully.";
} else {
    echo "Failed to send email with attachment.";
}

echo "sending email 2";
// send email
if (mail($to, $subject, $message2, $headers)) {
    echo "Email with attachment sent successfully.";
} else {
    echo "Failed to send email with attachment.";
}
?>

