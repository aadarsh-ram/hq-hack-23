import React, { useEffect, useState } from "react";
import { resultProps } from "./types";
import styles from "./ResultsPage.module.css"
import Resultcard from "../ResultCard/ResultCard";
import ResultRow from "../ResultRow/ResultRow";
import { Apiurls } from "../../utils/content";
import { Grid } from "@mui/material";


const Result : resultProps = {
    name : "Some name",
    education : "Some education",
    location : "Some location",
}


const ResultsPage = () => {

    const [results,setresults] = useState<resultProps[]>([Result,Result,Result,Result,Result,Result,Result,Result]);

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
            fetch(encodeURI(`${Apiurls[3].url}?keywords=${(jd.keywords)}&offset=1`),
                {
                    method:'GET',
                    headers:{
                        'accept':'application/json'
                    }
                }
            ).then(async(res)=>{
                let candidates = await(res.json());
                let result = candidates.map((candidate: any)=>{
                    let candidateData = {
                        name : candidate.name,
                        education : candidate.education,
                        location : candidate.location,
                        experience : ''
                    }
                    const experience : any = [];
                    candidate.resumeCardItems.map((item: any)=>{
                        experience.push(item.title+' - '+item.location);
                    })
                    candidateData['experience'] = experience.join('\n');
                    return candidateData;
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
        <Grid container 
            style={{marginTop: "4%", marginLeft: 2, overflowY: "scroll", alignItems: "stretch"}} 
            spacing={2}
            className={styles.pageContainer}>
            {
                results.map((result,index)=>{
                    return <Grid item xs={3}>
                        <Resultcard data={result}/>
                    </Grid>
                })
            }
        </Grid>
    );
}
 
export default ResultsPage;