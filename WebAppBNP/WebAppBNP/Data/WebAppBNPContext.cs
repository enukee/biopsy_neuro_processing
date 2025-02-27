using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using WebAppBNP.Data;

namespace WebAppBNP.Data
{
    public class WebAppBNPContext(DbContextOptions<WebAppBNPContext> options) : IdentityDbContext<WebAppBNPUser>(options)
    {
    }
}
