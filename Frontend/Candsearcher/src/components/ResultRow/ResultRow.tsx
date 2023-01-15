import React from "react";
import Resultcard from "../ResultCard/ResultCard";
import { resultProps } from "../ResultsPage/types";
import styles from "./ResultRow.module.css"

type Resultrowprops = {
    row : resultProps[];
}

const ResultRow = (props : Resultrowprops) => {
    return ( 
        <div className={styles.resultContainer}>
            <Resultcard data={props.row[0]} />
            <Resultcard data={props.row[1]} />
            <Resultcard data={props.row[2]} />
            <Resultcard data={props.row[3]} />
        </div>
    );
}
 
export default ResultRow;