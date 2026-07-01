using Microsoft.EntityFrameworkCore;
using RecomendationSystem.Models.Entities;

namespace RecomendationSystem.Data
{
    public class ApplicationContext : DbContext
    {
        public DbSet<Sdg> Sdgs { get; set; }

        public ApplicationContext(DbContextOptions<ApplicationContext> options) : base(options)
        {
            Database.EnsureCreated();
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Sdg>()
                .HasKey(x => new { x.CompanyId, x.Sdg_number });
        }
    }
}
