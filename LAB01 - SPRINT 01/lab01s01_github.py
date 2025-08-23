import os
import requests
import json
from datetime import datetime, timezone
from collections import Counter, defaultdict
import csv
import statistics

class GitHubRepositoryAnalyzer:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {token}',  
            'Content-Type': 'application/json'   
        }
        self.url = 'https://api.github.com/graphql' 
        
    def create_graphql_query(self, after_cursor=None):
        """
        Cria a query GraphQL para buscar repositórios populares com todas as métricas necessárias
        """
        after_clause = f', after: "{after_cursor}"' if after_cursor else ""
        
        query = f"""
        query {{
          search(query: "stars:>1000 sort:stars-desc", type: REPOSITORY, first: 20{after_clause}) {{
            pageInfo {{
              endCursor
              hasNextPage
            }}
            nodes {{
              ... on Repository {{
                name
                owner {{
                  login
                }}
                stargazerCount
                createdAt
                updatedAt
                primaryLanguage {{
                  name
                }}
                pullRequests(states: MERGED) {{
                  totalCount
                }}
                releases {{
                  totalCount
                }}
                issues {{
                  totalCount
                }}
                closedIssues: issues(states: CLOSED) {{
                  totalCount
                }}
                url
                description
              }}
            }}
          }}
        }}
        """
        return query
    
    def fetch_repositories(self, total_repos=100):
        repositories = []
        after_cursor = None
        
        print("Coletando dados dos repositórios...")
        
        while len(repositories) < total_repos:
            query = self.create_graphql_query(after_cursor)
            
            try:
                response = requests.post(
                    self.url,
                    json={'query': query},
                    headers=self.headers,
                    timeout=30
                )
                
                if response.status_code != 200:
                    print(f"Erro na requisição: {response.status_code}")
                    print(response.text)
                    break
                    
                data = response.json()
                
                if 'errors' in data:
                    print(f"Erro na query: {data['errors']}")
                    break
                    
                search_results = data['data']['search']
                repositories.extend(search_results['nodes'])
                
                print(f"Coletados {len(repositories)} repositórios...")
                
                if not search_results['pageInfo']['hasNextPage']:
                    break
                    
                after_cursor = search_results['pageInfo']['endCursor']
                
            except requests.exceptions.RequestException as e:
                print(f"Erro de conexão: {e}")
                break
        
        return repositories[:total_repos]
    
    def process_data(self, repositories):
        processed_data = []
        current_date = datetime.now(timezone.utc)
        
        for repo in repositories:
            # RQ01: Idade do repositório
            created_date = datetime.fromisoformat(repo['createdAt'].replace('Z', '+00:00'))
            age_days = (current_date - created_date).days
            
            # RQ02: Pull requests aceitas
            merged_prs = repo['pullRequests']['totalCount']
            
            # RQ03: Total de releases
            total_releases = repo['releases']['totalCount']
            
            # RQ04: Tempo até última atualização
            updated_date = datetime.fromisoformat(repo['updatedAt'].replace('Z', '+00:00'))
            days_since_update = (current_date - updated_date).days
            
            # RQ05: Linguagem primária
            primary_language = repo['primaryLanguage']['name'] if repo['primaryLanguage'] else 'Unknown'
            
            # RQ06: Percentual de issues fechadas
            total_issues = repo['issues']['totalCount']
            closed_issues = repo['closedIssues']['totalCount']
            closed_issues_ratio = (closed_issues / total_issues * 100) if total_issues > 0 else 0
            
            processed_data.append({
                'name': repo['name'],
                'owner': repo['owner']['login'],
                'stars': repo['stargazerCount'],
                'age_days': age_days,
                'merged_prs': merged_prs,
                'total_releases': total_releases,
                'days_since_update': days_since_update,
                'primary_language': primary_language,
                'total_issues': total_issues,
                'closed_issues': closed_issues,
                'closed_issues_ratio': closed_issues_ratio,
                'url': repo['url'],
                'description': repo['description']
            })
        
        return processed_data
    
    def calculate_stats(self, values):
        """
        Calcula estatísticas básicas para uma lista de valores
        """
        if not values:
            return {'mean': 0, 'median': 0, 'std': 0, 'min': 0, 'max': 0}
        
        return {
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'std': statistics.stdev(values) if len(values) > 1 else 0,
            'min': min(values),
            'max': max(values)
        }
    
    def analyze_rq01(self, data):
        # RQ01: Idade dos repositórios
        print("\n" + "="*50)
        print("RQ01: Sistemas populares são maduros/antigos?")
        print("="*50)
        
        # Lista com as idades em dias
        age_values = [repo['age_days'] for repo in data]
        # Convertendo pra anos (365.25 por causa dos anos bissextos)
        age_years = [days / 365.25 for days in age_values]
        stats = self.calculate_stats(age_years)
        
        print(f"Idade média dos repositórios: {stats['mean']:.2f} anos")
        print(f"Mediana da idade: {stats['median']:.2f} anos")
        print(f"Desvio padrão: {stats['std']:.2f} anos")
        print(f"Idade mínima: {stats['min']:.2f} anos")
        print(f"Idade máxima: {stats['max']:.2f} anos")
        
        # Categorização
        mature_repos = sum(1 for repo in data if repo['age_days'] > 365.25 * 5)
        print(f"\nRepositórios com mais de 5 anos: {mature_repos} ({mature_repos/len(data)*100:.1f}%)")
        
        return stats
    
    def analyze_rq02(self, data):
        print("\n" + "="*50)
        print("RQ02: Sistemas populares recebem muita contribuição externa?")
        print("="*50)
        
        # pega todos os PRs merged
        pr_values = [repo['merged_prs'] for repo in data]
        stats = self.calculate_stats(pr_values)  # calcula as estatísticas básicas
        
        print(f"Média de PRs aceitos: {stats['mean']:.2f}")
        print(f"Mediana de PRs aceitos: {stats['median']:.2f}")
        print(f"Desvio padrão: {stats['std']:.2f}")
        print(f"Máximo de PRs: {int(stats['max'])}")
        print(f"Mínimo de PRs: {int(stats['min'])}")
        
        high_contribution = sum(1 for repo in data if repo['merged_prs'] > stats['median'])
        print(f"\nRepositórios acima da mediana: {high_contribution} ({high_contribution/len(data)*100:.1f}%)")
        
        return stats
    
    def analyze_rq03(self, data):
        """
        RQ03: Sistemas populares lançam releases com frequência?
        """
        print("\n" + "="*50)
        print("RQ03: Sistemas populares lançam releases com frequência?")
        print("="*50)
        
        release_values = [repo['total_releases'] for repo in data]
        stats = self.calculate_stats(release_values)
        
        print(f"Média de releases: {stats['mean']:.2f}")
        print(f"Mediana de releases: {stats['median']:.2f}")
        print(f"Desvio padrão: {stats['std']:.2f}")
        print(f"Máximo de releases: {int(stats['max'])}")
        print(f"Mínimo de releases: {int(stats['min'])}")
        
        active_releasing = sum(1 for repo in data if repo['total_releases'] > 0)
        print(f"\nRepositórios com pelo menos 1 release: {active_releasing} ({active_releasing/len(data)*100:.1f}%)")
        
        return stats
    
    def analyze_rq04(self, data):
        """
        RQ04: Sistemas populares são atualizados com frequência?
        """
        print("\n" + "="*50)
        print("RQ04: Sistemas populares são atualizados com frequência?")
        print("="*50)
        
        update_values = [repo['days_since_update'] for repo in data]
        stats = self.calculate_stats(update_values)
        
        print(f"Média de dias desde última atualização: {stats['mean']:.2f}")
        print(f"Mediana: {stats['median']:.2f} dias")
        print(f"Desvio padrão: {stats['std']:.2f}")
        print(f"Máximo: {int(stats['max'])} dias")
        print(f"Mínimo: {int(stats['min'])} dias")
        
        recently_updated = sum(1 for repo in data if repo['days_since_update'] <= 30)
        print(f"\nRepositórios atualizados nos últimos 30 dias: {recently_updated} ({recently_updated/len(data)*100:.1f}%)")
        
        return stats
    
    def analyze_rq05(self, data):
        """
        RQ05: Sistemas populares são escritos nas linguagens mais populares?
        """
        print("\n" + "="*50)
        print("RQ05: Sistemas populares são escritos nas linguagens mais populares?")
        print("="*50)
        
        languages = [repo['primary_language'] for repo in data]
        language_counts = Counter(languages)
        
        print("Top 10 linguagens mais usadas:")
        for i, (lang, count) in enumerate(language_counts.most_common(10), 1):
            percentage = (count / len(data)) * 100
            print(f"{i:2d}. {lang}: {count} repositórios ({percentage:.1f}%)")
        
        return language_counts
    
    def analyze_rq06(self, data):
        """
        RQ06: Sistemas populares possuem um alto percentual de issues fechadas?
        """
        print("\n" + "="*50)
        print("RQ06: Sistemas populares possuem um alto percentual de issues fechadas?")
        print("="*50)
        
        # Remove repositórios sem issues para análise
        repos_with_issues = [repo for repo in data if repo['total_issues'] > 0]
        
        if not repos_with_issues:
            print("Nenhum repositório com issues encontrado.")
            return {}
        
        ratios = [repo['closed_issues_ratio'] for repo in repos_with_issues]
        stats = self.calculate_stats(ratios)
        
        print(f"Repositórios com issues: {len(repos_with_issues)} de {len(data)}")
        print(f"Percentual médio de issues fechadas: {stats['mean']:.2f}%")
        print(f"Mediana: {stats['median']:.2f}%")
        print(f"Desvio padrão: {stats['std']:.2f}%")
        print(f"Máximo: {stats['max']:.2f}%")
        print(f"Mínimo: {stats['min']:.2f}%")
        
        high_closure_rate = sum(1 for repo in repos_with_issues if repo['closed_issues_ratio'] > 80)
        print(f"\nRepositórios com mais de 80% de issues fechadas: {high_closure_rate} ({high_closure_rate/len(repos_with_issues)*100:.1f}%)")
        
        return stats
    
    def analyze_rq07_bonus(self, data):
        """
        RQ07 (Bônus): Sistemas escritos em linguagens mais populares recebem mais 
        contribuição externa, lançam mais releases e são atualizados com mais frequência?
        """
        print("\n" + "="*60)
        print("RQ07 (BÔNUS): Análise por linguagem")
        print("="*60)
        
        # Agrupa dados por linguagem
        lang_data = defaultdict(list)
        for repo in data:
            lang_data[repo['primary_language']].append(repo)
        
        # Considera apenas as top 5 linguagens para análise
        language_counts = Counter(repo['primary_language'] for repo in data)
        top_languages = [lang for lang, count in language_counts.most_common(5)]
        
        print("\nAnálise das top 5 linguagens:")
        print("="*40)
        
        for lang in top_languages:
            repos = lang_data[lang]
            count = len(repos)
            
            prs = [repo['merged_prs'] for repo in repos]
            releases = [repo['total_releases'] for repo in repos]
            updates = [repo['days_since_update'] for repo in repos]
            
            pr_stats = self.calculate_stats(prs)
            release_stats = self.calculate_stats(releases)
            update_stats = self.calculate_stats(updates)
            
            print(f"\n{lang} ({count} repositórios):")
            print(f"  PRs aceitos - Média: {pr_stats['mean']:.2f}, Mediana: {pr_stats['median']:.2f}")
            print(f"  Releases - Média: {release_stats['mean']:.2f}, Mediana: {release_stats['median']:.2f}")
            print(f"  Dias desde update - Média: {update_stats['mean']:.2f}, Mediana: {update_stats['median']:.2f}")
        
        return lang_data
    
    def create_simple_charts(self, data):
        print("\n" + "="*60)
        print("VISUALIZAÇÕES SIMPLES")
        print("="*60)
        
        # RQ05: Top linguagens (gráfico de barras ASCII)
        print("\nRQ05: Top 10 Linguagens (Gráfico de Barras ASCII)")
        print("-" * 50)
        
        languages = [repo['primary_language'] for repo in data]
        language_counts = Counter(languages)
        
        max_count = max(language_counts.values())
        scale_factor = 40 / max_count  # Escala para 40 caracteres
        
        for i, (lang, count) in enumerate(language_counts.most_common(10), 1):
            bar_length = int(count * scale_factor)
            bar = "█" * bar_length
            percentage = (count / len(data)) * 100
            print(f"{i:2d}. {lang:<15} {bar} {count} ({percentage:.1f}%)")
        
        # RQ01: Distribuição da idade
        print("\nRQ01: Distribuição da Idade (em anos)")
        print("-" * 50)
        
        ages = [repo['age_days'] / 365.25 for repo in data]
        
        # Cria histograma simples
        bins = [0, 2, 4, 6, 8, 10, 15, 20]
        bin_labels = ["0-2", "2-4", "4-6", "6-8", "8-10", "10-15", "15+"]
        
        for i in range(len(bins) - 1):
            count = sum(1 for age in ages if bins[i] <= age < bins[i+1])
            if i == len(bins) - 2:  # Último bin inclui valores maiores
                count = sum(1 for age in ages if age >= bins[i])
            
            bar_length = int(count * 40 / len(data))  # Escala para 40 caracteres
            bar = "█" * bar_length
            percentage = (count / len(data)) * 100
            print(f"{bin_labels[i]:<6} anos {bar} {count} ({percentage:.1f}%)")
    
    def save_data_csv(self, data, filename='github_repositories_data.csv'):
        """
        Salva os dados coletados em CSV
        """
        if not data:
            print("Nenhum dado para salvar.")
            return
        
        fieldnames = data[0].keys()
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            print(f"\nDados salvos em: {filename}")
            
        except Exception as e:
            print(f"Erro ao salvar arquivo CSV: {e}")
    
    def save_summary_report(self, data, filename='github_analysis_report.txt'):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("RELATÓRIO DE ANÁLISE - REPOSITÓRIOS POPULARES DO GITHUB\n")
                f.write("=" * 60 + "\n\n")
                
                f.write(f"Data da análise: {datetime.now().strftime('%Y-%m-%d')}\n")
                f.write(f"Total de repositórios analisados: {len(data)}\n\n")
                
                # Resumo por RQ
                f.write("RESUMO DAS RESEARCH QUESTIONS:\n")
                f.write("-" * 40 + "\n\n")
                
                # RQ01
                ages = [repo['age_days'] / 365.25 for repo in data]
                age_stats = self.calculate_stats(ages)
                f.write(f"RQ01 - Maturidade:\n")
                f.write(f"  Idade média: {age_stats['mean']:.2f} anos\n")
                f.write(f"  Repositórios com +5 anos: {sum(1 for a in ages if a > 5)} ({sum(1 for a in ages if a > 5)/len(ages)*100:.1f}%)\n\n")
                
                # RQ02
                prs = [repo['merged_prs'] for repo in data]
                pr_stats = self.calculate_stats(prs)
                f.write(f"RQ02 - Contribuições:\n")
                f.write(f"  Média de PRs aceitos: {pr_stats['mean']:.2f}\n")
                f.write(f"  Mediana de PRs: {pr_stats['median']:.2f}\n\n")
                
                # RQ03
                releases = [repo['total_releases'] for repo in data]
                release_stats = self.calculate_stats(releases)
                f.write(f"RQ03 - Releases:\n")
                f.write(f"  Média de releases: {release_stats['mean']:.2f}\n")
                f.write(f"  Repos com releases: {sum(1 for r in releases if r > 0)} ({sum(1 for r in releases if r > 0)/len(releases)*100:.1f}%)\n\n")
                
                # RQ04
                updates = [repo['days_since_update'] for repo in data]
                update_stats = self.calculate_stats(updates)
                f.write(f"RQ04 - Atualizações:\n")
                f.write(f"  Média dias desde update: {update_stats['mean']:.2f}\n")
                f.write(f"  Atualizados em 30 dias: {sum(1 for u in updates if u <= 30)} ({sum(1 for u in updates if u <= 30)/len(updates)*100:.1f}%)\n\n")
                
                # RQ05
                languages = Counter(repo['primary_language'] for repo in data)
                f.write(f"RQ05 - Top 5 Linguagens:\n")
                for i, (lang, count) in enumerate(languages.most_common(5), 1):
                    f.write(f"  {i}. {lang}: {count} repos ({count/len(data)*100:.1f}%)\n")
                f.write("\n")
                
                # RQ06
                repos_with_issues = [repo for repo in data if repo['total_issues'] > 0]
                if repos_with_issues:
                    ratios = [repo['closed_issues_ratio'] for repo in repos_with_issues]
                    ratio_stats = self.calculate_stats(ratios)
                    f.write(f"RQ06 - Issues Fechadas:\n")
                    f.write(f"  Média de fechamento: {ratio_stats['mean']:.2f}%\n")
                    f.write(f"  Repos com +80% fechadas: {sum(1 for r in ratios if r > 80)} ({sum(1 for r in ratios if r > 80)/len(ratios)*100:.1f}%)\n\n")
                
            print(f"Relatório salvo em: {filename}")
            
        except Exception as e:
            print(f"Erro ao salvar relatório: {e}")
    
    def run_complete_analysis(self, total_repos=100):
        print("INICIANDO ANÁLISE COMPLETA DOS REPOSITÓRIOS DO GITHUB")
        print("=" * 60)
        
        # 1. Coleta de dados
        repositories = self.fetch_repositories(total_repos)
        
        if not repositories:
            print("Erro: Nenhum repositório foi coletado.")
            return None
        
        # 2. Processamento
        data = self.process_data(repositories)
        
        # 3. Análises das RQs
        self.analyze_rq01(data)
        self.analyze_rq02(data)
        self.analyze_rq03(data)
        self.analyze_rq04(data)
        self.analyze_rq05(data)
        self.analyze_rq06(data)
        
        # 4. Bônus
        self.analyze_rq07_bonus(data)
        
        # 5. Visualizações simples
        self.create_simple_charts(data)
        
        # 6. Salvar dados e relatório
        self.save_data_csv(data)
        self.save_summary_report(data)
        
        print("\n" + "="*60)
        print("ANÁLISE COMPLETA FINALIZADA!")
        print("="*60)
        print(f"Arquivos gerados:")
        print(f"  - github_repositories_data.csv (dados completos)")
        print(f"  - github_analysis_report.txt (relatório resumido)")
        
        return data

if __name__ == "__main__":
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  
    
    if not GITHUB_TOKEN:  
        try:
            with open('LAB01 - SPRINT 01/config.json') as f:
                config = json.load(f)
                GITHUB_TOKEN = config['github_token']
        except FileNotFoundError: 
            print("Arquivo de configuração não encontrado. Defina a variável de ambiente GITHUB_TOKEN ou crie o arquivo config.json.")
        
    analyzer = GitHubRepositoryAnalyzer(GITHUB_TOKEN)
    
    try:
        results = analyzer.run_complete_analysis(1000)  # analisa 100 repos
        
        if results:
            print(f"\n Sucesso")
        else:
            print("Erro")
            
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        
    input("\nPressione Enter para sair...")