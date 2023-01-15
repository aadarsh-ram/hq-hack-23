import React, { useEffect, useState } from "react";
import { resultProps } from "./types";
import styles from "./ResultsPage.module.css"
import Resultcard from "../ResultCard/ResultCard";
import ResultRow from "../ResultRow/ResultRow";


const Result : resultProps = {
    name : "Shubham Agarwal",
    jobTitle : "NIT Tiruchirapalli"
}


const ResultsPage = () => {

    const [results,setresults] = useState<resultProps[]>([Result,Result,Result,Result,Result,Result,Result,Result,]);
    const cards : number[]=[1,2,3,4,5,6,7,8];
    const[pagenum,setpageNum] = useState<number>(0);

    return ( 
        <div className={styles.pageContainer}>
            <ResultRow row={results} />
            <ResultRow row={results} />
        </div>
    );
}
 
export default ResultsPage;