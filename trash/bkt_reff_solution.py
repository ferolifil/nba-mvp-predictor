from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType

client.players_season_totals(
    season_end_year=1980, 
    output_type=OutputType.CSV, 
    output_file_path="./1979_1980_player_season_totals.csv"
)

client.players_advanced_season_totals(
    season_end_year=1980,
    output_type=OutputType.CSV,
    output_file_path="./1979_1980_advanced_player_season_totals.csv"
)