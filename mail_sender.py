from fastapi import APIRouter, Form, Depends, Request, status
from fastapi.responses import RedirectResponse
from botocore.exceptions import ClientError
from dotenv import dotenv_values
from dataclasses import dataclass

import pyotp
import boto3
import jwt
import time

CFG = dotenv_values(".env")

@dataclass
class User():
    username: str = Form(...)
    mail_address: str = Form(...)
    password: str = Form(...)


SENDER = "samiberke2003@gmail.com"
AWS_REGION = "us-east-1"
SUBJECT = "Amazon SES Test (SDK for Python)"
CHARSET = "UTF-8"


jwtSecret = "berke"


def otpGenerator():
    timeout_interval = CFG["TIMEOUT_INTERVAL"]
    totp = pyotp.TOTP(CFG["OTP_SECRET"], interval=int(timeout_interval))
    code = totp.now()
    print(code)
    return code

def jwtEncoder(obj):
    encoded = jwt.encode(obj, jwtSecret, algorithm="HS256")
    return encoded

def jwtDecoder(encoded):
    decoded = jwt.decode(encoded, jwtSecret, algorithms=["HS256"])
    return decoded

def mailSender(jwt, otp_code, recipient):
    print(jwt)
    print(otp_code)
    BODY_HTML = """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" style="font-family:arial, 'helvetica neue', helvetica, sans-serif">
    <head>
    <meta charset="UTF-8">
    <meta content="width=device-width, initial-scale=1" name="viewport">
    <meta name="x-apple-disable-message-reformatting">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta content="telephone=no" name="format-detection">
    <title>New message 2</title><!--[if (mso 16)]>
        <style type="text/css">
        a {text-decoration: none;}
        </style>
        <![endif]--><!--[if gte mso 9]><style>sup { font-size: 100% !important; }</style><![endif]--><!--[if gte mso 9]>
    <xml>
        <o:OfficeDocumentSettings>
        <o:AllowPNG></o:AllowPNG>
        <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
    </xml>
    <![endif]--><!--[if !mso]><!-- -->
    <link href="https://fonts.googleapis.com/css2?family=Imprima&display=swap" rel="stylesheet"><!--<![endif]-->
    <style type="text/css">
    #outlook a {
        padding:0;
    }
    .es-button {
        mso-style-priority:100!important;
        text-decoration:none!important;
    }
    a[x-apple-data-detectors] {
        color:inherit!important;
        text-decoration:none!important;
        font-size:inherit!important;
        font-family:inherit!important;
        font-weight:inherit!important;
        line-height:inherit!important;
    }
    .es-desk-hidden {
        display:none;
        float:left;
        overflow:hidden;
        width:0;
        max-height:0;
        line-height:0;
        mso-hide:all;
    }
    @media only screen and (max-width:600px) {p, ul li, ol li, a { line-height:150%!important } h1, h2, h3, h1 a, h2 a, h3 a { line-height:120% } h1 { font-size:30px!important; text-align:left } h2 { font-size:24px!important; text-align:left } h3 { font-size:20px!important; text-align:left } .es-header-body h1 a, .es-content-body h1 a, .es-footer-body h1 a { font-size:30px!important; text-align:left } .es-header-body h2 a, .es-content-body h2 a, .es-footer-body h2 a { font-size:24px!important; text-align:left } .es-header-body h3 a, .es-content-body h3 a, .es-footer-body h3 a { font-size:20px!important; text-align:left } .es-menu td a { font-size:14px!important } .es-header-body p, .es-header-body ul li, .es-header-body ol li, .es-header-body a { font-size:14px!important } .es-content-body p, .es-content-body ul li, .es-content-body ol li, .es-content-body a { font-size:14px!important } .es-footer-body p, .es-footer-body ul li, .es-footer-body ol li, .es-footer-body a { font-size:14px!important } .es-infoblock p, .es-infoblock ul li, .es-infoblock ol li, .es-infoblock a { font-size:12px!important } *[class="gmail-fix"] { display:none!important } .es-m-txt-c, .es-m-txt-c h1, .es-m-txt-c h2, .es-m-txt-c h3 { text-align:center!important } .es-m-txt-r, .es-m-txt-r h1, .es-m-txt-r h2, .es-m-txt-r h3 { text-align:right!important } .es-m-txt-l, .es-m-txt-l h1, .es-m-txt-l h2, .es-m-txt-l h3 { text-align:left!important } .es-m-txt-r img, .es-m-txt-c img, .es-m-txt-l img { display:inline!important } .es-button-border { display:block!important } a.es-button, button.es-button { font-size:18px!important; display:block!important; border-right-width:0px!important; border-left-width:0px!important; border-top-width:15px!important; border-bottom-width:15px!important } .es-adaptive table, .es-left, .es-right { width:100%!important } .es-content table, .es-header table, .es-footer table, .es-content, .es-footer, .es-header { width:100%!important; max-width:600px!important } .es-adapt-td { display:block!important; width:100%!important } .adapt-img { width:100%!important; height:auto!important } .es-m-p0 { padding:0px!important } .es-m-p0r { padding-right:0px!important } .es-m-p0l { padding-left:0px!important } .es-m-p0t { padding-top:0px!important } .es-m-p0b { padding-bottom:0!important } .es-m-p20b { padding-bottom:20px!important } .es-mobile-hidden, .es-hidden { display:none!important } tr.es-desk-hidden, td.es-desk-hidden, table.es-desk-hidden { width:auto!important; overflow:visible!important; float:none!important; max-height:inherit!important; line-height:inherit!important } tr.es-desk-hidden { display:table-row!important } table.es-desk-hidden { display:table!important } td.es-desk-menu-hidden { display:table-cell!important } .es-menu td { width:1%!important } table.es-table-not-adapt, .esd-block-html table { width:auto!important } table.es-social { display:inline-block!important } table.es-social td { display:inline-block!important } .es-desk-hidden { display:table-row!important; width:auto!important; overflow:visible!important; max-height:inherit!important } }
    </style>
    </head>
    <body data-new-gr-c-s-loaded="8.905.0" style="width:100%;font-family:arial, 'helvetica neue', helvetica, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">
    <div class="es-wrapper-color" style="background-color:#FFFFFF"><!--[if gte mso 9]>
                <v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
                    <v:fill type="tile" color="#ffffff"></v:fill>
                </v:background>
            <![endif]-->
    <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top;background-color:#FFFFFF">
        <tr>
        <td valign="top" style="padding:0;Margin:0">
        <table class="es-footer" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
            <tr>
            <td align="center" style="padding:0;Margin:0">
            <table class="es-footer-body" cellspacing="0" cellpadding="0" bgcolor="#bcb8b1" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;width:600px">
                <tr>
                <td align="left" style="Margin:0;padding-top:20px;padding-bottom:20px;padding-left:40px;padding-right:40px">
                <table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                    <tr>
                    <td valign="top" align="center" style="padding:0;Margin:0;width:520px">
                    <table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                        <tr>
                        <td style="padding:0;Margin:0;display:none" align="center"></td>
                        </tr>
                    </table></td>
                    </tr>
                </table></td>
                </tr>
            </table></td>
            </tr>
        </table>
        <table class="es-content" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
            <tr>
            <td align="center" style="padding:0;Margin:0">
            <table class="es-content-body" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#EFEFEF;border-radius:20px 20px 0 0;width:600px" cellspacing="0" cellpadding="0" bgcolor="#efefef" align="center">
                <tr>
                <td align="left" style="padding:0;Margin:0;padding-left:40px;padding-right:40px">
                <table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                    <tr>
                    <td valign="top" align="center" style="padding:0;Margin:0;width:520px">
                    <table width="100%" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                        <tr>
                        <td class="es-m-txt-c" style="padding:0;Margin:0;font-size:0px" align="left"><img src="https://uploads-ssl.webflow.com/62d5695106896ecf208fc5eb/643efed950a2943924d39299_grid_0-removebg-preview(1).png" alt="Confirm email" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;border-radius:100px;font-size:12px" title="Confirm email" width="100"></td>
                        </tr>
                    </table></td>
                    </tr>
                </table></td>
                </tr>
                <tr>
                <td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:40px;padding-right:40px">
                <table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                    <tr>
                    <td valign="top" align="center" style="padding:0;Margin:0;width:520px">
                    <table style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:separate;border-spacing:0px;background-color:#fafafa;border-radius:10px" width="100%" cellspacing="0" cellpadding="0" bgcolor="#fafafa" role="presentation">
                        <tr>
                        <td align="left" style="padding:30px;Margin:0"><h3 style="Margin:0;line-height:34px;mso-line-height-rule:exactly;font-family:Imprima, Arial, sans-serif;font-size:28px;font-style:normal;font-weight:bold;color:#2D3142">Welcome,</h3><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Imprima, Arial, sans-serif;line-height:27px;color:#2D3142;font-size:18px"><br></p><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Imprima, Arial, sans-serif;line-height:27px;color:#2D3142;font-size:18px">You're receiving this message because you recently signed up for a account.<br>To confirm your account, please enter OTP code.<br>OTP code: &lt;"""+otp_code+"""&gt;<br><a href='http://127.0.0.1:8000/jwt/"""+jwt+"""'> Or Click Here! </a></p></td>
                        </tr>
                    </table></td>
                    </tr>
                </table></td>
                </tr>
            </table></td>
            </tr>
        </table>
        <table class="es-content" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
            <tr>
            <td align="center" style="padding:0;Margin:0">
            <table class="es-content-body" cellspacing="0" cellpadding="0" bgcolor="#efefef" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#EFEFEF;width:600px">
                <tr>
                <td align="left" style="padding:0;Margin:0;padding-left:40px;padding-right:40px">
                <table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                    <tr>
                    <td valign="top" align="center" style="padding:0;Margin:0;width:520px">
                    <table width="100%" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                        <tr>
                        <td align="left" style="padding:10px;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Imprima, Arial, sans-serif;line-height:27px;color:#2D3142;font-size:18px">Thanks,<br>Sweephy</p></td>
                        </tr>
                        <tr>
                        <td style="padding:0;Margin:0;padding-bottom:20px;padding-top:40px;font-size:0" align="center">
                        <table width="100%" height="100%" cellspacing="0" cellpadding="0" border="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                            <tr>
                            <td style="padding:0;Margin:0;border-bottom:1px solid #666666;background:unset;height:1px;width:100%;margin:0px"></td>
                            </tr>
                        </table></td>
                        </tr>
                    </table></td>
                    </tr>
                </table></td>
                </tr>
            </table></td>
            </tr>
        </table>
        <table class="es-content" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
            <tr>
            <td align="center" style="padding:0;Margin:0">
            <table class="es-content-body" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#EFEFEF;border-radius:0 0 20px 20px;width:600px" cellspacing="0" cellpadding="0" bgcolor="#efefef" align="center">
                <tr>
                <td class="esdev-adapt-off" align="left" style="Margin:0;padding-top:20px;padding-bottom:20px;padding-left:40px;padding-right:40px">
                <table class="esdev-mso-table" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:520px">
                    <tr>
                    <td class="esdev-mso-td" valign="top" style="padding:0;Margin:0">
                    <table class="es-left" cellspacing="0" cellpadding="0" align="left" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left">
                        <tr>
                        <td valign="top" align="center" style="padding:0;Margin:0;width:47px">
                        <table width="100%" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                            <tr>
                            <td class="es-m-txt-l" style="padding:0;Margin:0;font-size:0px" align="center"><a target="_blank" href="https://sweephy.com" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#2D3142;font-size:18px"><img src="https://uploads-ssl.webflow.com/62d5695106896ecf208fc5eb/643efed950a2943924d39299_grid_0-removebg-preview(1).png" alt="Demo" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" title="Demo" width="47"></a></td>
                            </tr>
                        </table></td>
                        </tr>
                    </table></td>
                    <td style="padding:0;Margin:0;width:20px"></td>
                    <td class="esdev-mso-td" valign="top" style="padding:0;Margin:0">
                    <table class="es-right" cellspacing="0" cellpadding="0" align="right" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right">
                        <tr>
                        <td valign="top" align="center" style="padding:0;Margin:0;width:453px">
                        <table width="100%" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                            <tr>
                            <td align="left" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Imprima, Arial, sans-serif;line-height:24px;color:#2D3142;font-size:16px">This code expire in 24 hours. If you need any help, please contact with us.</p></td>
                            </tr>
                        </table></td>
                        </tr>
                    </table></td>
                    </tr>
                </table></td>
                </tr>
            </table></td>
            </tr>
        </table>
        <table class="es-footer" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
            <tr>
            <td align="center" style="padding:0;Margin:0">
            <table class="es-footer-body" cellspacing="0" cellpadding="0" bgcolor="#bcb8b1" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;width:600px">
                <tr>
                <td align="left" style="Margin:0;padding-top:10px;padding-bottom:15px;padding-left:20px;padding-right:20px">
                <table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                    <tr>
                    <td align="left" style="padding:0;Margin:0;width:560px">
                    <table width="100%" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                        <tr>
                        <td class="es-m-txt-c" style="padding:0;Margin:0;padding-bottom:20px;font-size:0px" align="center"><a target="_blank" href="https://sweephy.com" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#2D3142;font-size:14px"><img src="https://uploads-ssl.webflow.com/62d5695106896ecf208fc5eb/643efed950a2943924d39299_grid_0-removebg-preview(1).png" alt="Logo" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" title="Logo" height="90"></a></td>
                        </tr>
                        <tr>
                        <td class="es-m-txt-c" style="padding:0;Margin:0;padding-top:10px;padding-bottom:20px;font-size:0" align="center">
                        <table class="es-table-not-adapt es-social" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                            <tr>
                            <td valign="top" align="center" style="padding:0;Margin:0;padding-right:5px"><a target="_blank" href="https://twitter.com/sweephy" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#2D3142;font-size:14px"><img src="https://dzlnqr.stripocdn.email/content/assets/img/social-icons/logo-black/twitter-logo-black.png" alt="Tw" title="Twitter" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                            <td valign="top" align="center" style="padding:0;Margin:0"><a target="_blank" href="https://www.linkedin.com/company/sweephy/" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#2D3142;font-size:14px"><img src="https://dzlnqr.stripocdn.email/content/assets/img/social-icons/logo-black/linkedin-logo-black.png" alt="In" title="Linkedin" height="24" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td>
                            </tr>
                        </table></td>
                        </tr>
                        <tr>
                        <td align="center" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Imprima, Arial, sans-serif;line-height:20px;color:#2D3142;font-size:13px"><a target="_blank" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:none;color:#2D3142;font-size:14px" href="https://www.sweephy.com/privacy-policy">Privacy Policy</a><br></p></td>
                        </tr>
                        <tr>
                        <td align="center" style="padding:0;Margin:0;padding-top:20px"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Imprima, Arial, sans-serif;line-height:21px;color:#2D3142;font-size:14px"><a target="_blank" href="" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#2D3142;font-size:14px"></a>Copyright © 2023 Sweephy</p></td>
                        </tr>
                    </table></td>
                    </tr>
                </table></td>
                </tr>
            </table></td>
            </tr>
        </table>
        <table class="es-footer" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
            <tr>
            <td align="center" style="padding:0;Margin:0">
            <table class="es-footer-body" cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;width:600px">
                <tr>
                <td align="left" style="padding:20px;Margin:0">
                <table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                    <tr>
                    <td align="left" style="padding:0;Margin:0;width:560px">
                    <table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                        <tr>
                        <td style="padding:0;Margin:0;display:none" align="center"></td>
                        </tr>
                    </table></td>
                    </tr>
                </table></td>
                </tr>
            </table></td>
            </tr>
        </table></td>
        </tr>
    </table>
    </div>
    </body>
    </html>
                """
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                )
    client = boto3.client('ses',region_name=AWS_REGION, 
                          aws_access_key_id=CFG["AWS_ACCESS_KEY"],
                          aws_secret_access_key=CFG["AWS_SECRET_ACCESS_KEY"],)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )	
    except ClientError as e:
        return e.response['Error']['Message']
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
    return


router = APIRouter()

@router.post("/send_mail")
async def FunctionName(user_info: User = Depends()):
    #Hash password first.
    hash_password = user_info.password
    obj = {"username": user_info.username, "mail_address": user_info.mail_address, "hash_password": hash_password, "timestamp": int(time.time()), "used": False}
    encoded = jwtEncoder(obj)
    mailSender(encoded, otpGenerator(), user_info.mail_address)
    return RedirectResponse(url="http://127.0.0.1:8000/verification", status_code=status.HTTP_302_FOUND)


@router.get("/jwt/{encoded}")
async def FunctionName(request: Request, encoded: str):
    decoded = jwtDecoder(encoded)
    if time.time() - decoded["timestamp"] < 300:
        user_info = {"username": decoded["username"], "mail_address": decoded["mail_address"], "hash_password": decoded["hash_password"]}
        user_info = user_info
        request.app.database["users"].insert_one(user_info)
        return RedirectResponse(url="http://127.0.0.1:8000/", status_code=status.HTTP_302_FOUND)
    else:
        return {"message": "Timeout!"}