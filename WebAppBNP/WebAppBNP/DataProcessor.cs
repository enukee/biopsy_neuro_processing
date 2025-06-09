using Microsoft.AspNetCore.Components.Forms;
using System.Drawing;
using static System.Net.WebRequestMethods;

namespace WebAppBNP
{
    public class DataProcessor
    {
        public struct ReceivedData
        {
            public string imageUrl;
            public Report report;
        }

        private const string url = "http://127.0.0.1:5000";

        public static async Task<ReceivedData> ProcessingImage(HttpClient Http, IBrowserFile file)
        {
            ReceivedData data = new ReceivedData();

            // Формирование тела запроса
            var content = new MultipartFormDataContent();
            var streamContent = new StreamContent(file.OpenReadStream(104857600));
            content.Add(streamContent, "file", file.Name);

            Console.WriteLine("Отправка файла на сервер...");

            // Отправка запроса
            var response = await Http.PostAsync(url + "/process-image", content);

            if (response.IsSuccessStatusCode)
            {
                // Сохранение имени обработанного файла
                var contentDisposition = response.Content.Headers.ContentDisposition;
                var fileName = contentDisposition?.FileName;

                var processedImageBytes = await response.Content.ReadAsByteArrayAsync();
                data.imageUrl = $"data:image/jpg;base64,{Convert.ToBase64String(processedImageBytes)}";

                Console.WriteLine("Файл успешно загружен и обработан.");

                if (fileName is not null)
                {
                    // Получаем сырой JSON для отладки
                    var jsonResponse = await Http.GetStringAsync(url + $"/report/{Uri.EscapeDataString(fileName)}");
                    Console.WriteLine("Получение отчёта");

                    // Десериализуем JSON в объект Data
                    data.report = System.Text.Json.JsonSerializer.Deserialize<Report>(jsonResponse);
                }

                return data;
            }
            else
            {
                throw new Exception($"Ошибка: {response.StatusCode}");
            }
        }

        public static async Task<string> UploadPDFReport(HttpClient Http, Report report)
        {
            // Формирование тела запроса
            string json = System.Text.Json.JsonSerializer.Serialize(report,
            new System.Text.Json.JsonSerializerOptions { WriteIndented = true });
            var content = new StringContent(json, System.Text.Encoding.UTF8, "application/json");

            var response = await Http.PostAsync(url + "/report/pdf", content);
            if (response.IsSuccessStatusCode) {
                byte[] pdfBytes = await response.Content.ReadAsByteArrayAsync();
                var pdgReport = $"data:application/pdf;base64,{Convert.ToBase64String(pdfBytes)}";
                Console.WriteLine("PDF-файл загружен.");

                return pdgReport;
            }
            else
            {
                throw new Exception($"Ошибка: {response.StatusCode}");
            }
        }
    }
}
