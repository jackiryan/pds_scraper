"""
The MIT License (MIT)

Copyright (c) 2022, Jacqueline Ryan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import argparse
import re
import requests
import urllib.parse

from pds_scraper.url import check_url
from pds_scraper.mission import check_mission

def get_data_url(node_name: str, mission: str) -> str:
    """
    Determine the base URL for the PDS node on the provided sol.
    Return this URL as a string.

    :param node_name: Name of the PDS node to access.
    :param mission: Mission from which to scrape data. Default is Mars 2020.
    :return: A string containing the PDS URL down to mission data level
             (one directory above the package level)
    """
    # Check that the node name is a valid url, and add an origin string if necessary.
    node_url = check_url(node_name)
    # Check the mission name against a list of known names from the NAIF database.
    mission_pds_name = check_mission(mission)

    data_pkg_url = "/".join(node_url, mission_pds_name)
    return data_pkg_url


def scrape_sol(sol_int: int,
               node_name: str = "pds-imaging.jpl.nasa.gov",
               mission: str = "MARS 2020", 
               edrs: bool = False,
               rdrs: bool = False,
               meshes: bool = False) -> bool:
    """
    High-level function performing the work necessary to scrape EDRs, RDRs, and meshes
    from one sol on a given PDS node for a Mars surface mission. Tested missions are:
        * Mars 2020, also known as Perseverance.
        * Mars Science Laboratory (MSL), also known as Curiosity.
        * Mars Exploration Rovers, Spirit and Opportunity.
    
    :param sol_int: User-provided sol which will be found in the PDS node.
    :param node_name: A host name, with or without an origin, that describes the URL of a
                      PDS imaging node.
    :param mission: A string denoting the mission from which to download data. Input will
                    be sanitized and checked against officially-recognized NAIF IDs.
    :param edrs: Flag to decide whether to download EDRs
    :param rdrs: Flag to decide whether to download RDRs
    :param meshes: Flag to decide whether to download meshes
    :return: A boolean indicating whether the data was successfully synced.
    """
    # Get the base URL on the PDS that will be scraped for data. This function sanitizes
    # inputs.
    pds_url = get_data_url(node_name, mission)
    print(f"Accessing data from {pds_url}...")

    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("sol", type=int, help="Sol from which to scrape data.")
    parser.add_argument("-n", "--node-name", type=str,
                        help="Name of the PDS node from which to obtain the data.")
    parser.add_argument("--mission", type=str,
                        help="Name of the mission of interest.")
    parser.add_argument("-e", "--dl-edrs", action="store_true",
                        help="Download EDRs for the given sol.")
    parser.add_argument("-r", "--dl-rdrs", action="store_true",
                        help="Download RDRs for the given sol.")
    parser.add_argument("-m", "--dl-meshes", action="store_true",
                        help="Download mesh data from the given sol.")
    args = parser.parse_args()

    # The default node for this script is the JPL node. This is the primary node
    # that receives archive data from Mars surface missions.
    node_name = args.node_name or "pds-imaging.jpl.nasa.gov"
    # This script was developed for Mars 2020-related work, so that is the default mission.
    mission = args.mission or "MARS 2020"

    scrape_sol(args.sol, node_name, mission,
               args.dl_edrs, args.dl_rdrs,
               args.dl_meshes)

if __name__ == "__main__":
    main()