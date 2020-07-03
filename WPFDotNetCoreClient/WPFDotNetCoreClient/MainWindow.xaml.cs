using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using Newtonsoft.Json;
using System.Net.Security;
using System.Security.Cryptography.X509Certificates;
using System.Net.Http;
using System.DirectoryServices;
using System.Collections.ObjectModel;

namespace WPFDotNetCoreClient
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public class SaveItem
        {
            public string Address, Account, Password, Text;
        }
        public class SearchItem
        {
            public string Address { get; set; }
            public string Account { get; set; }
            public string Password { get; set; }
            public string Date { get; set; }
            public string Text { get; set; }
        }
        public class ForSearchItem
        {
            public string Key, Keyword;
        }
        public class ForUpdateItem
        {
            public string Date { get; set; }
            public string Text { get; set; }
        }
        public string __Window_Title = "Account Manager Client With C#";
        public string __Author = "Anest";
        public string __Version = "Jul 3, 2020.";
        public string __url;  // http ://127.0.0.1:5000
        public SaveItem save_item = null;
        public ForSearchItem for_search_item = null;
        public ForUpdateItem for_update_item = null;
        public string AccountStr = "";
        public string PasswordStr = "";
        public string GetHTTPRequest(string url)
        {
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
            request.Method = "GET";
            request.ContentType = "application/json";
            request.Timeout = 4000;
            HttpWebResponse response = null;
            try
            {
                response = (HttpWebResponse)request.GetResponse();
            }
            catch (Exception e)
            {
                MessageBox.Show(e.ToString());
            }
            Stream myResponseStream = response.GetResponseStream();
            StreamReader myStreamReader = new StreamReader(myResponseStream, Encoding.GetEncoding("utf-8"));
            string retString = myStreamReader.ReadToEnd();
            myStreamReader.Close();
            myResponseStream.Close();
            return retString;
        }
        public static string PostHttpRequest(string url, Dictionary<string, string> param)
        {
            string result = null;
            using (HttpClient httpClient = new HttpClient(new HttpClientHandler
            {
                AutomaticDecompression = DecompressionMethods.None,
                ClientCertificateOptions = ClientCertificateOption.Automatic
            }))
                try
                {
                    {
                        httpClient.BaseAddress = new Uri(url);
                        FormUrlEncodedContent content = new FormUrlEncodedContent(param);
                        result = httpClient.PostAsync(url, content).Result.Content.ReadAsStringAsync().Result;
                    }
                }
                catch (Exception e)
                {
                    MessageBox.Show(e.ToString());
                }
            return result;
        }

        private static bool CheckValidationResult(object sender, X509Certificate certificate, X509Chain chain, SslPolicyErrors errors)
        {
            return true; //总是接受   
        }

        //https
        public static HttpWebResponse CreatePostHttpResponse(string url, IDictionary<string, string> parameters, Encoding charset)
        {
            HttpWebRequest request = null;
            ServicePointManager.ServerCertificateValidationCallback = new RemoteCertificateValidationCallback(CheckValidationResult);
            request = WebRequest.Create(url) as HttpWebRequest;
            request.ProtocolVersion = HttpVersion.Version10;
            request.Method = "POST";
            request.ContentType = "application/x-www-form-urlencoded";
            if (!(parameters == null || parameters.Count == 0))
            {
                StringBuilder buffer = new StringBuilder();
                int i = 0;
                foreach (string key in parameters.Keys)
                {
                    if (i > 0)
                    {
                        buffer.AppendFormat("&{0}={1}", key, parameters[key]);
                    }
                    else
                    {
                        buffer.AppendFormat("{0}={1}", key, parameters[key]);
                    }
                    i++;
                }
                byte[] data = charset.GetBytes(buffer.ToString());
                using (Stream stream = request.GetRequestStream())
                {
                    stream.Write(data, 0, data.Length);
                }
            }
            return request.GetResponse() as HttpWebResponse;
        }
        public MainWindow()
        {
            InitializeComponent();
            __url = ServerLink_btn.Text;
        }
        private void About_btn_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show(
                string.Format(@"Author: {0}
Version:{1}", __Author, __Version),
                __Window_Title);
        }

        private void ServerLink_btn_LostFocus(object sender, RoutedEventArgs e)
        {
            __url = ServerLink_btn.Text;
        }

        private async void Generate_btn_ClickAsync(object sender, RoutedEventArgs e)
        {
            Generator_Generate_btn.IsEnabled = false;
            if (Generator_IsFixedAccount.IsChecked.Value == false)
            {
                await Task.Run(new Action(Generate_btn_Click__GetAccount));
            }
            await Task.Run(new Action(Generate_btn_Click__GetPassword));
            Generator_Generate_btn.IsEnabled = true;
        }
        public void Generate_btn_Click__GetAccount()
        {
            string retString = GetHTTPRequest(string.Format("{0}/getAccount/", __url));
            Dispatcher.BeginInvoke(new Action(() => Generator_Account.Text = retString));
        }
        public void Generate_btn_Click__GetPassword()
        {
            string retString = GetHTTPRequest(string.Format("{0}/getPW/", __url));
            Dictionary<string, string> r = JsonConvert.DeserializeObject<Dictionary<string, string>>(retString);
            Dispatcher.BeginInvoke(new Action(() => Generator_Password_lv1.Text = r["pw1"]));
            Dispatcher.BeginInvoke(new Action(() => Generator_Password_lv2.Text = r["pw2"]));
            Dispatcher.BeginInvoke(new Action(() => Generator_Password_lv3.Text = r["pw3"]));
            Dispatcher.BeginInvoke(new Action(() => Generator_Password_lv_max.Text = r["pwmax"]));

        }

        private async void Generator_SaveResult_btn_ClickAsync(object sender, RoutedEventArgs e)
        {
            Generator_SaveResult_btn.IsEnabled = false;
            save_item = new SaveItem();
            save_item.Address = Generator_Address.Text;
            save_item.Account = Generator_Account.Text;
            save_item.Text = Generator_Text.Text;
            RadioButton checkBtn = Generator_Select.Children.OfType<RadioButton>().FirstOrDefault(r => r.IsChecked.Value);
            switch (checkBtn.Name[checkBtn.Name.Length - 1])
            {
                case '1':
                    save_item.Password = Generator_Password_lv1.Text;
                    break;
                case '2':
                    save_item.Password = Generator_Password_lv2.Text;
                    break;
                case '3':
                    save_item.Password = Generator_Password_lv3.Text;
                    break;
                case 'x':
                    save_item.Password = Generator_Password_lv_max.Text;
                    break;
            }
            await Task.Run(new Action(Generator_SaveResult_btn_Click__Work));
            Generator_SaveResult_btn.IsEnabled = true;
        }
        public void Generator_SaveResult_btn_Click__Work()
        {
            Dictionary<string, string> pd = new Dictionary<string, string>();
            pd.Add("AddressStr", save_item.Address);
            pd.Add("AccountStr", save_item.Account);
            pd.Add("password", save_item.Password);
            pd.Add("Text", save_item.Text);
            try
            {
                string rs = PostHttpRequest(string.Format("{0}/Save_Result_to_sql/", __url), pd);
                pd = null;
                MessageBox.Show(rs);
            }
            catch (Exception e)
            {
                MessageBox.Show(e.ToString());
            }
        }

        private async void Seach_Search_btn_ClickAsync(object sender, RoutedEventArgs e)
        {
            Seach_Search_btn.IsEnabled = false;
            for_search_item = new ForSearchItem();
            RadioButton checkBtn = Search_Select.Children.OfType<RadioButton>().FirstOrDefault(r => r.IsChecked.Value);
            switch (checkBtn.Name[checkBtn.Name.Length - 1])
            {
                case '0':
                    for_search_item.Key = "0";
                    for_search_item.Keyword = Search_Address.Text;
                    break;
                case '1':
                    for_search_item.Key = "1";
                    for_search_item.Keyword = Search_Account.Text;
                    break;
                case '2':
                    for_search_item.Key = "2";
                    for_search_item.Keyword = Search_Password.Text;
                    break;
                case '3':
                    for_search_item.Key = "3";
                    for_search_item.Keyword = Search_Text.Text;
                    break;
            }
            try
            {
                await Task.Run(new Action(Seach_Search_btn_Click__Work));
            }
            catch (Exception e2)
            {
                MessageBox.Show(e2.ToString());
            }
            Seach_Search_btn.IsEnabled = true;
        }
        public void Seach_Search_btn_Click__Work()
        {
            Dictionary<string, string> pd = new Dictionary<string, string>();
            pd.Add("key", for_search_item.Key);
            pd.Add("keyword", for_search_item.Keyword);
            pd.Add("language", "en-us");
            string rs = null;
            try
            {
                rs = PostHttpRequest(string.Format("{0}/Search_item", __url), pd);
            }
            catch (Exception e)
            {
                MessageBox.Show(e.ToString());
            }
            pd = null;
            string[][] r = JsonConvert.DeserializeObject<string[][]>(rs);
            ObservableCollection<SearchItem> searchItems = new ObservableCollection<SearchItem>();
            for (int i = 0; i < r.Length - 1; i++)
            {
                searchItems.Add(new SearchItem()
                {
                    Address = r[i][0],
                    Account = r[i][1],
                    Password = r[i][2],
                    Date = r[i][3],
                    Text = r[i][4]
                });
            }
            searchItems.Add(new SearchItem() { Address = "Update Date", Account = r[r.Length - 1][0], Password = " ", Date = " ", Text = " " });
            Dispatcher.BeginInvoke(new Action(() => Search_Search_Result.ItemsSource = searchItems));
            for_search_item = null;

        }

        private async void Update_Search_btn_ClickAsync(object sender, RoutedEventArgs e)
        {
            for_update_item = new ForUpdateItem();
            for_update_item.Date = Update_Date.Text;
            for_update_item.Text = Update_Text.Text;
            try
            {
                await Task.Run(new Action(Update_Search_btn_Click__Work));
            }
            catch (Exception e2)
            {
                MessageBox.Show(e2.ToString());
            }
        }
        public void Update_Search_btn_Click__Work()
        {
            Dictionary<string, string> pd = new Dictionary<string, string>();
            pd.Add("DateStr", for_update_item.Date);
            pd.Add("TextStr", for_update_item.Text);
            try
            {
                string rs = PostHttpRequest(string.Format("{0}/Update_Text", __url), pd);
                MessageBox.Show(rs,__Window_Title);
            }
            catch (Exception e)
            {
                MessageBox.Show(e.ToString());
            }
            pd = null;
        }
    }
}
