//https://kb.arubacloud.com/en/api/computing/manipulating-the-items/creating-a-cloud-server.aspx

// IWsEndUser.GetPreConfiguredPackages Method JAVA)
public static String GetPreConfiguredPackages(IWsEndUser client) {
    StringBuilder sb = new StringBuilder();
    try {
        GetPreConfiguredPackagesRequest request = new GetPreConfiguredPackagesRequest();
        request.setHypervisorType(HypervisorTypes.ALL);

        WsResultOfArrayOfCloudPackage result = client.getPreConfiguredPackages(request);

        if (result.isSuccess()) {
            sb.append("Configured Packages: ");
            for (CloudPackage cp: result.getValue()) {
              sb.append("\nPackageID: " + cp.getPackageID());
              sb.append("\n\t- Price: " + cp.getPrice());
              sb.append("\n\t- Description: " + cp.getDescriptions());
              sb.append("\n\t- Cpu Quantity: " + cp.getCpuQuantity());
              sb.append("\n\t- Billing Type: " + cp.getBillingType());
              sb.append("\n\t- Hdd0Quantity: " + cp.getHdd0Quantity());
            }
        } else {    
            throw new Exception(result.getResultMessage());
        }
    } catch (Exception ex) { 
      System.out.println(ex);
    }
    return sb.toString();
}

https://kb.arubacloud.com/en/api/computing/advanced-manipulation-of-the-items/initialize-a-cloud-server-smart.aspx

//IWsEndUser.SetEnqueueReinitializeServer Method (Java)
    private static void SetEnqueueReinitializeServer(
        IWsEndUser client, int serverId, String administratorPassword) {
        try {
            ReinitializeServerRequest request = new ReinitializeServerRequest();
            request.ServerId = serverId;
            request.AdministratorPassword = administratorPassword;
            WsResult result = client.SetEnqueueReinitializeServer(request);

            //if the call fails; it relaunches the error indicating the message
            if (!result.Success)
               throw new Exception(result.getResultMessage());
        } catch (Exception ex) {
             System.out.println(ex);
        }
    }
// https://sourceforge.net/p/java-openpanel/code-0/HEAD/tree/trunk/java-OpenPanel/

