import React from "react";
import withStyles from "@material-ui/core/styles/withStyles";
import Typography from "@material-ui/core/Typography";
import corpusLibrary from "./corpusLibrary";


const useStyles = () => ({
    root: {
        maxWidth: '800px',
        // display: 'flex'
    },
    title: {
        marginLeft: '8px',
        marginTop: '10px',
    },
    outputText: {
        marginLeft: '8px',
        // color: '#ef395a',
        marginTop: '10px',
        // border: '1px solid black'
    }
});

const Corpus = ({ classes, randNo }) => {
    return (
        randNo < 500 && <div className={classes.root}>
            <div className={classes.title}>
                <Typography variant="h5">
                    Corpus
                </Typography>
            </div>
            <div className={classes.outputText}>
                <Typography variant="body1">
                    "{corpusLibrary[String(randNo)]['sentence']}"
                </Typography>
            </div>
        </div>
    )
}

export default withStyles(useStyles)(Corpus);
