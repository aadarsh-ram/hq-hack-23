import React, { useEffect, useState } from "react";
import { resultProps } from "./types";
import styles from "./ResultsPage.module.css"
import Resultcard from "../ResultCard/ResultCard";
import ResultRow from "../ResultRow/ResultRow";


const Result : resultProps = {
    jobTitle : "Sales manager",
    location : "Delhi",
    currentJob: "ICICI Bank",
}

const Result2 : resultProps = {
    jobTitle : "Sales manager",
    location : "Dehradun",
    currentJob : "Idea cellular Ltd.",
}
const Result3 : resultProps = {
    jobTitle : "Sales Executive",
    location : "Navi mumbai",
    currentJob : "Novasatam Food Pvt limited "
}
const Result4 : resultProps = {
    jobTitle : "Tele Sales Executive",
    location : "Amritsar",
    currentJob : "Nextday marketing Solutions"
}
const Result5 : resultProps = {
    jobTitle : "Sales Manager",
    location : "Calicut",
    currentJob : "Toy triangle"
}
const Result6 : resultProps = {
    jobTitle : "Sales manager",
    location : "Jamshedpur",
    currentJob : "Kapsons Industries Pvt Ltd"
}

const Result7 : resultProps = {
    jobTitle : "Sales Executive",
    location : "Bangalore",
    currentJob : "Vedantu"
}
const Result8 : resultProps = {
    jobTitle : "Sales Executive",
    location : "SantaCruz",
    currentJob : "QuesCorp"
}


const ResultsPage = () => {

    const [results,setresults] = useState<resultProps[]>([Result,Result2,Result3,Result4,Result5,Result6,Result7,Result8]);
    const[pagenum,setpageNum] = useState<number>(0);

    return ( 
        <div className={styles.pageContainer}>
            <ResultRow row={results} />
            <ResultRow row={results} />
        </div>
    );
}
 
export default ResultsPage;