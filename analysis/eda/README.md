# Notes

## Survey
Cornell IT turned off export options for Qualtrics? I can't embed the condition variables, so they exported survey data is in order, but we need the QID mapping to condition.
If you export the questionnaire from Qualtrics you can use this [fx](https://fx.wtf/) command to generate the file [QID_map](./src/Data/QID_map.json) which will need to be regenerated if the survey is changed.

```bash
cat QUALTRICS.qsf | fx 'Object.entries(this.SurveyElements[0].Payload).map(([k,v])=>({
  block: v.Description,
  flowID: v.Flow
  questionIDs: v.BlockElements.filter(e => e.Type === "Question").map(e => e.QuestionID)
}))' > QID_map.json
```

```bash
cat QUALTRICS.qsf |  fx '.SurveyElements[1].Payload.Flow.find(a=>a.FlowID=="FL_65").Flow.map(({FlowID, Description})=>({FlowID, Description}))' > FlowMap.json
```

## Tooling

I'm using some slightly more esoteric tooling, feel free to use notebooks, etc. but trying some things out. I can help convert to more standard tooling, most things are cross compatible.

- [fx](https://fx.wtf/) for dealing with JSON
- [Rye](https://rye.astral.sh/) for environment and package management
- [marimo](https://marimo.io/) as a Jupyter notebook alternative
- [Vega-Altair](https://altair-viz.github.io/) for plotting
- [Polars](https://pola.rs/) instead of Pandas

## Notes
- high pass filter on the imu data
- use STD or RMS rather than raw magnitude

Running [example_participant.py](./src/example_participant.py) requires updating the max output bytes run 

`export MARIMO_OUTPUT_MAX_BYTES=10_000_000`

then 

`marimo edit eda/src/example_participant.py`


## measures
- nback delay?
