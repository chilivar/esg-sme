using Microsoft.EntityFrameworkCore;
using System.ComponentModel.Design;

namespace RecomendationSystem.Models.Entities
{
    public class Sdg
    {
        public int CompanyId { get; set; }
        
        public int Sdg_number {  get; set; }

        public double Value { get; set; }

        public Sdg() { }

        public Sdg(int companyId, int sdgNumber, double value)
        {
            CompanyId = companyId;
            Sdg_number = sdgNumber;
            Value = value;
        }
    }
}
