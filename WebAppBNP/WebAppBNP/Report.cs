namespace WebAppBNP
{
    public class Report
    {
        public List<double> ObjectsArea { get; set; }
        public List<List<int>> ObjectsCenter { get; set; }

        public Report()
        {
            ObjectsArea = new List<double>();
            ObjectsCenter = new List<List<int>>();
        }

        public void AddReport(Report report)
        {
            var area = report.ObjectsArea;
            var center = report.ObjectsCenter;
            if (area is not null)
            {
                ObjectsArea.AddRange(area);
            }
            if (center is not null)
            {
                ObjectsCenter.AddRange(center);
            }
        }

        public void Clear()
        {
            ObjectsArea.Clear();
            ObjectsCenter.Clear();
        }
    }

    public class Center
    {
        public int X { get; set; }
        public int Y { get; set; }
    }
}
