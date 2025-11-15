import dns.resolver
import pandas as pd
import os
import time
import random

def identify_email_service(mx_servers):
    """Enhanced email service detection including web hosts"""
    mx_servers_lower = [server.lower() for server in mx_servers]
    
    # Google Workspace / Gmail
    if any('google' in server or 'aspmx.l.google.com' in server for server in mx_servers_lower):
        return 'Google Workspace'
    
    # Microsoft 365 / Outlook
    elif any('outlook' in server or 'protection.outlook' in server or 'mail.protection' in server for server in mx_servers_lower):
        return 'Microsoft 365'
    
    # Amazon SES
    elif any('amazonaws' in server or 'ses' in server for server in mx_servers_lower):
        return 'Amazon SES'
    
    # Web Hosting Services
    elif any('secureserver' in server or 'godaddy' in server for server in mx_servers_lower):
        return 'GoDaddy Email'
    
    elif any('bluehost' in server for server in mx_servers_lower):
        return 'Bluehost Email'
    
    elif any('hostgator' in server for server in mx_servers_lower):
        return 'HostGator Email'
    
    elif any('siteground' in server for server in mx_servers_lower):
        return 'SiteGround Email'
    
    elif any('namecheap' in server or 'privateemail' in server for server in mx_servers_lower):
        return 'Namecheap Email'
    
    elif any('dreamhost' in server for server in mx_servers_lower):
        return 'DreamHost Email'
    
    elif any('cpanel' in server or 'cpane' in server for server in mx_servers_lower):
        return 'cPanel Hosting'
    
    elif any('cloudflare' in server for server in mx_servers_lower):
        return 'Cloudflare Email'
    
    # Other Email Services
    elif any('zoho' in server for server in mx_servers_lower):
        return 'Zoho Mail'
    
    elif any('yahoo' in server for server in mx_servers_lower):
        return 'Yahoo Mail'
    
    elif any('protonmail' in server or 'proton' in server for server in mx_servers_lower):
        return 'ProtonMail'
    
    elif any('fastmail' in server for server in mx_servers_lower):
        return 'Fastmail'
    
    elif any('sendgrid' in server for server in mx_servers_lower):
        return 'SendGrid'
    
    elif any('mailgun' in server for server in mx_servers_lower):
        return 'Mailgun'
    
    elif any('postmark' in server for server in mx_servers_lower):
        return 'Postmark'
    
    # Additional providers for better accuracy
    elif any('rackspace' in server for server in mx_servers_lower):
        return 'Rackspace Email'
    
    elif any('ionos' in server or '1and1' in server for server in mx_servers_lower):
        return 'IONOS Email'
    
    elif any('network solutions' in server or 'netsol' in server for server in mx_servers_lower):
        return 'Network Solutions'
    
    elif any('wix' in server for server in mx_servers_lower):
        return 'Wix Email'
    
    elif any('squarespace' in server for server in mx_servers_lower):
        return 'Squarespace Email'
    
    # Generic hosting patterns
    elif any('mx' in server and ('host' in server or 'server' in server or 'web' in server) for server in mx_servers_lower):
        return 'Generic Web Hosting'
    
    else:
        return 'Custom/Unknown'

def analyzer(input_file, output_file, email_column='Email'):
    try:
        # Read input file
        if input_file.endswith('.csv'):
            df = pd.read_csv(input_file)
        else:
            df = pd.read_excel(input_file)
        
        print(f"📧 Processing {len(df)} emails from {input_file}")
        
        # Check if email column exists
        if email_column not in df.columns:
            print(f"❌ Error: Column '{email_column}' not found!")
            print(f"Available columns: {list(df.columns)}")
            return
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return
    
    results = []
    domain_cache = {}
    processed_count = 0
    failed_lookups = 0
    
    # Configure DNS resolver with timeout and retry
    resolver = dns.resolver.Resolver()
    resolver.timeout = 10  # 10 second timeout
    resolver.lifetime = 10  # 10 second total lifetime
    
    for index, row in df.iterrows():
        email = row[email_column]
        
        if pd.isna(email) or '@' not in str(email):
            results.append({**row.to_dict(), 'email_service': 'Invalid Email'})
            continue
        
        domain = str(email).split('@')[-1].lower().strip()
        
        if domain not in domain_cache:
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    mx_records = resolver.resolve(domain, 'MX')
                    mx_servers = [str(mx.exchange).rstrip('.') for mx in mx_records]  # Remove trailing dots
                    
                    # Use enhanced identification
                    service = identify_email_service(mx_servers)
                    domain_cache[domain] = service
                    break  # Success, exit retry loop
                    
                except dns.resolver.NXDOMAIN:
                    domain_cache[domain] = 'Domain Not Found'
                    break
                except dns.resolver.NoAnswer:
                    domain_cache[domain] = 'No MX Records'
                    break
                except dns.resolver.Timeout:
                    if attempt < max_retries - 1:
                        print(f"   ⏳ DNS timeout for {domain}, retrying...")
                        time.sleep(1)  # Wait before retry
                        continue
                    else:
                        domain_cache[domain] = 'DNS Timeout'
                        failed_lookups += 1
                        break
                except dns.resolver.NoNameservers:
                    domain_cache[domain] = 'No Nameservers'
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"   ⚠️ DNS error for {domain}: {e}, retrying...")
                        time.sleep(1)
                        continue
                    else:
                        domain_cache[domain] = f'DNS Error'
                        failed_lookups += 1
                        break
            
            # Small delay to avoid DNS rate limiting
            time.sleep(0.1 + random.uniform(0, 0.2))
        
        results.append({**row.to_dict(), 'email_service': domain_cache[domain]})
        processed_count += 1
        
        # Progress indicator
        if processed_count % 20 == 0:  # More frequent updates
            print(f"   Processed {processed_count}/{len(df)} emails...")
    
    # Create output DataFrame
    output_df = pd.DataFrame(results)
    
    # Write output file
    try:
        if output_file.endswith('.csv'):
            output_df.to_csv(output_file, index=False)
        else:
            output_df.to_excel(output_file, index=False)
        
        print(f"✅ Results saved to {output_file}")
        
        # Show detailed summary
        summary = output_df['email_service'].value_counts()
        print(f"\n📊 PROCESSING COMPLETE")
        print(f"📧 Total emails processed: {len(df)}")
        print(f"❌ Failed DNS lookups: {failed_lookups}")
        print("=" * 50)
        
        # Group by service type
        cloud_services = ['Google Workspace', 'Microsoft 365']
        web_hosting = ['GoDaddy Email', 'Bluehost Email', 'HostGator Email', 'SiteGround Email', 
                      'Namecheap Email', 'DreamHost Email', 'cPanel Hosting', 'Generic Web Hosting',
                      'Rackspace Email', 'IONOS Email', 'Network Solutions', 'Wix Email', 'Squarespace Email']
        transactional = ['Amazon SES', 'SendGrid', 'Mailgun', 'Postmark']
        other_services = ['Zoho Mail', 'Yahoo Mail', 'ProtonMail', 'Fastmail', 'Cloudflare Email']
        error_categories = ['Domain Not Found', 'No MX Records', 'DNS Timeout', 'No Nameservers', 'DNS Error', 'Invalid Email']
        
        categories = {
            'Cloud Email Suites': [],
            'Web Hosting Email': [],
            'Transactional Email': [],
            'Other Email Services': [],
            'Custom/Unknown': [],
            'Errors & Issues': []
        }
        
        for service, count in summary.items():
            if service in cloud_services:
                categories['Cloud Email Suites'].append((service, count))
            elif service in web_hosting:
                categories['Web Hosting Email'].append((service, count))
            elif service in transactional:
                categories['Transactional Email'].append((service, count))
            elif service in other_services:
                categories['Other Email Services'].append((service, count))
            elif service in error_categories:
                categories['Errors & Issues'].append((service, count))
            elif 'Custom' in service or 'Unknown' in service:
                categories['Custom/Unknown'].append((service, count))
            else:
                categories['Custom/Unknown'].append((service, count))
        
        # Print categorized results
        total_accounted = 0
        for category, services in categories.items():
            if services:
                category_total = sum(count for _, count in services)
                total_accounted += category_total
                print(f"\n{category} ({category_total}):")
                for service, count in services:
                    percentage = (count / len(df)) * 100
                    print(f"  └─ {service}: {count} emails ({percentage:.1f}%)")
        
        print("=" * 50)
        print(f"📊 Successfully identified: {total_accounted - summary.get('Invalid Email', 0)}/{len(df)} emails")
            
    except Exception as e:
        print(f"❌ Error saving file: {e}")


# Test it directly
if __name__ == "__main__":
    analyzer(
        input_file='Agricultural-Contractors-Huntsville-AL-Companies.xlsx',
        output_file='sorted_results.xlsx',
        email_column='Email'
    )