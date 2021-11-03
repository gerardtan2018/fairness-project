import React from "react";
import withStyles from "@material-ui/core/styles/withStyles";
import Typography from "@material-ui/core/Typography";
import {calculateEditDistance, wordErrorRate} from "word-error-rate";
import corpusLibrary from "./corpusLibrary";

const useStyles = () => ({
  root: {
    maxWidth: '800px',
    // display: 'flex'
  },
  outputText: {
    marginLeft: '8px',
    color: '#ef395a',
  }
});

const Metrics = ({classes, transcribedText, interimTranscribedText, isRecording, randNo}) => {
  if ((transcribedText.length === 0 && interimTranscribedText.length === 0) || isRecording) {
    return <Typography variant="body1"></Typography>;
  }

  return (
    transcribedText[0].length > 0 && <div className={classes.root}>
      <Typography variant="body1">Word Error Rate</Typography>
      <Typography className={classes.outputText} variant="body1">{wordErrorRate(corpusLibrary[String(randNo)]['sentence'].replace(/[^a-zA-Z ]/g, ""), transcribedText[0].replace(/[^a-zA-Z ]/g, ""))}</Typography>
    </div>
  )
}

export default withStyles(useStyles)(Metrics);
