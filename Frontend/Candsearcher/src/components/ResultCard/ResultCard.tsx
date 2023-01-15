import React from "react";
import styles from './ResultCard.module.css'
import { resultProps } from "../ResultsPage/types";

type ResultCardprops = {
    data : resultProps
}


const Resultcard = (props : ResultCardprops ) => {
    return ( 
        <div className={styles.cardContainer}>
            <div className={styles.name}>
                {props.data.name}
            </div>
            <div className={styles.jobtitle}>
                {props.data.jobTitle}
            </div>
            <div className={styles.showbutton}>
                Show more
            </div>
        </div>
    );
}
 
export default Resultcard;