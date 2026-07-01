using RecomendationSystem.Models.Entities;

namespace RecomendationSystem.Services
{
    public class CategoriesService : ICategoriesService
    {
        public List<Category> GetResults(List<Sdg> sdgs, string language)
        {
            var category1 = new Category { Category_name = "Economic", Sdg_numbers = new List<int> { 8, 9, 12 } };
            var category2 = new Category { Category_name = "Social", Sdg_numbers = new List<int> { 1, 3, 4, 5, 8, 10 } };
            var category3 = new Category { Category_name = "Environmental", Sdg_numbers = new List<int> { 6, 7, 12, 13, 15 } };
            var category4 = new Category { Category_name = "Technological", Sdg_numbers = new List<int> { 9, 12, 8, 4 } };

            if (language == "ru")
            {
                category1.Category_name = "Экономический";
                category2.Category_name = "Социальный";
                category3.Category_name = "Экологический";
                category4.Category_name = "Технологический";
            }
            else if (language == "kz")
            {
                category1.Category_name = "Экономикалық";
                category2.Category_name = "Әлеуметтік";
                category3.Category_name = "Экологиялық";
                category4.Category_name = "Технологиялық";
            }

            var weights1 = new List<double> { 0.5, 0.33, 0.17 };
            var weights2 = new List<double> { 0.2857, 0.2381, 0.1905, 0.1429, 0.0952, 0.0476 };
            var weights3 = new List<double> { 0.333, 0.267, 0.2, 0.133, 0.067 };
            var weights4 = new List<double> { 0.4, 0.3, 0.2, 0.1 };

            category1.Value = CalculateCategoryValue(category1, sdgs, weights1);
            category2.Value = CalculateCategoryValue(category2, sdgs, weights2);
            category3.Value = CalculateCategoryValue(category3, sdgs, weights3);
            category4.Value = CalculateCategoryValue(category4, sdgs, weights4);

            return new List<Category> { category1, category2, category3, category4 };
        }

        private double CalculateCategoryValue(Category category, List<Sdg> sdgs, List<double> weights)
        {
            double value = 0;
            foreach (var sdg_number in category.Sdg_numbers)
            {
                var sdg = sdgs.Find(s => s.Sdg_number == sdg_number);
                if (sdg != null)
                {
                    int index = category.Sdg_numbers.IndexOf(sdg_number);
                    value += sdg.Value * weights[index];
                }
            }
            return value;
        }
    }
}
