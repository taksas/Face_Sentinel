using System;
using System.Threading.Tasks;

namespace WBF_API_ClassLibrary
{
    public class WBF_API_Class
    {


        public int Authorization()
        {
            return Authorization_Func().Result;
        }


        public async Task<int> Authorization_Func()
        {
            var available = await Windows.Security.Credentials.UI.UserConsentVerifier.CheckAvailabilityAsync();
            if (available == Windows.Security.Credentials.UI.UserConsentVerifierAvailability.Available)
            {
                var result = await Windows.Security.Credentials.UI.UserConsentVerifier.RequestVerificationAsync("Authorization Started");
                if (result == Windows.Security.Credentials.UI.UserConsentVerificationResult.Verified)
                {
                    return 0; // OK
                }
                else
                {
                    return 1; // NG
                }
            }
            else
            {
                return -1; // Error
            }
        }
    }
}
