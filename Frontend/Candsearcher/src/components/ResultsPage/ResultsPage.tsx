import React, { useEffect, useState } from "react";
import { resultProps } from "./types";
import styles from "./ResultsPage.module.css"
import Resultcard from "../ResultCard/ResultCard";
import ResultRow from "../ResultRow/ResultRow";
import { Apiurls } from "../../utils/content";


const Result : resultProps = {
    name : "Some name",
    education : "Some education",
    location : "Some location",
}

const Result2 : resultProps = {
    name : "Some name",
    education : "Some education",
    location : "Some location",
}
const Result3 : resultProps = {
    name : "Some name",
    education : "Some education",
    location : "Some location",
}
const Result4 : resultProps = {
    name : "Some name",
    education : "Some education",
    location : "Some location",
}


const ResultsPage = () => {

    const [results,setresults] = useState<resultProps[]>([Result,Result2,Result3,Result4]);

    useEffect(()=>{
        fetch(`${Apiurls[2].url}/1`,
            {
                method:'GET',
                headers:{
                    'accept':'application/json'
                }
            }
        ).then(async(response)=>{
            let jd = await(response.json())
            console.log(jd);
            fetch(encodeURI(`${Apiurls[3].url}?keywords=${(jd.keywords)}&offset=1`),
                {
                    method:'GET',
                    headers:{
                        'accept':'application/json'
                    }
                }
            ).then(async(res)=>{
                let candidates = await(res.json());
                console.log(candidates);
                let result = candidates.map((candidate: any)=>{
                    return {
                        name : candidate.name,
                        education : candidate.education,
                        location : candidate.location
                    }
                })
                setresults(result);
            }).catch((e)=>{
                console.log(e);
            })
        }).catch((e)=>{
            console.log(e)
        })
    },[])

    return ( 
        <div className={styles.pageContainer}>
            <ResultRow row={results} />
        </div>
    );
}
 
export default ResultsPage;