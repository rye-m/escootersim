import json
import polars as pl

def get_participant_data(id, survey_path):
    return pl.read_csv(survey_path).filter(pl.col('randomID')==str(id))

def get_flow_data(flow_path):
    with open(flow_path) as fm:
        flow_json = json.load(fm)
        flow_map = {i["FlowID"]: i["Description"] for i in flow_json}
    return flow_map

def get_order(participant_data, flow_map):
    session_order = [flow_map[a] for a in participant_data['FL_65_DO'][0].split('|')]
    return session_order