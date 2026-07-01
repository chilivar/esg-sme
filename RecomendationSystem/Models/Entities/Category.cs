namespace RecomendationSystem.Models.Entities
{
    public class Category
    {
        public required string Category_name { get; set; }

        public double Value { get; set; }

        public List<int> Sdg_numbers { get; set; }

        public Category() { }
    }
}
