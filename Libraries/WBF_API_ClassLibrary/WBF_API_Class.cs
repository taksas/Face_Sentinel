using System;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
using System.Diagnostics;
using System.Linq;

namespace WBF_API_ClassLibrary
{
    public class WBF_API_Class
    {



        [DllImport("user32", SetLastError = true)]
        private static extern IntPtr OpenInputDesktop(uint dwFlags,
                                                      bool fInherit,
                                                      uint dwDesiredAccess);





        public int authorization()
        {
            return authorization_func().Result;
        }


        public async Task<int> authorization_func()
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





        // Check if the workstation has been locked.
        public int IsWorkstationLocked()
        {
            bool locked = Process.GetProcessesByName("logonui").Any();

            if (locked) return 1;
            else return 0;
            
        }

       
    }

}
