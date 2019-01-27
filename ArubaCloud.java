// https://kb.arubacloud.com/en/api/common/connecting-to-the-apis.aspx
//   for Visual Studio 2010 and Netbeans 7
// Checked with Netbeans 8.2

import https.api_computing_cloud_it.wsenduser.IWsEndUser;
import https.api_computing_cloud_it.wsenduser.WsEndUser;
import javax.xml.ws.BindingProvider;

public class ArubaCloud {

    private static Boolean Login(IWsEndUser client, String aruba_user, String aruba_password) throws Exception {
      try { // https://kb.arubacloud.com/en/api/common/login-and-use-of-the-token.aspx
        ((BindingProvider)client).getRequestContext()
                .put(BindingProvider.USERNAME_PROPERTY, aruba_user);
        ((BindingProvider)client).getRequestContext()
                .put(BindingProvider.PASSWORD_PROPERTY, aruba_password);

        if (client.getUserAuthenticationToken(null).isSuccess()) {
          return true;
        } else {
          System.out.println(client.getUserAuthenticationToken(null).getResultMessage());
          return false;
        }
      } catch (SecurityException ex) {
          System.out.println(ex);
      } return false;
    }

    public static void main(String[] args) {
      String u = "AWI-11111";
      String p = "1111111111";
      int serverID=111111;
      try {
        IWsEndUser wsUser = new WsEndUser().getBasicHttpsEndpoint();
        Login(wsUser,u,p);
        System.out.println(
          wsUser.getCredit().getValue().getValue().toString());
        System.out.println(
          wsUser.getServerDetails(serverID).getValue().getName());
      } catch (Exception e) {
        System.out.println(e);
      }
    }
}
/*
https://kb.arubacloud.com/en/api/common/compatibility-of-the-platform.aspx

The platform uses Web Services to communicate requests to and from the Cloud Computing systems.
Aruba provides examples of use with .NET WCF (.NET 3.5 SP1 or higher) and JAVA.
The authentication system is WSIF, an extension for the SOAP standard.
*/
