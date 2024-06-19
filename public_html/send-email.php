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
$file = "images/gif0.gif";

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
$message = "--{$mime_boundary}\n" . "Content-Type: text/html; charset=\"UTF-8\"\n" . "Content-Transfer-Encoding: 7bit\n\n" . $htmlContent . "\n\n";

// Preparing attachment
if (!empty($file) > 0)
{
    if (is_file($file))
    {
        $message .= "--{$mime_boundary}\n";
        $fp = fopen($file, "rb");
        $data = fread($fp, filesize($file));

        fclose($fp);
        $data = chunk_split(base64_encode($data));
        $message .= "Content-Type: application/octet-stream; name=\"" . basename($file) . "\"\n" . "Content-Description: " . basename($file) . "\n" . "Content-Disposition: attachment;\n" . " filename=\"" . basename($file) . "\"; size=" . filesize($file) . ";\n" . "Content-Transfer-Encoding: base64\n\n" . $data . "\n\n";
    }
}

echo "sending email";
// send email
if (mail($to, $subject, $message, $headers)) {
    echo "Email with attachment sent successfully.";
} else {
    echo "Failed to send email with attachment.";
}
?>

