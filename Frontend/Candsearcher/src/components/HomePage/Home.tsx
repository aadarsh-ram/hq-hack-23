import * as React from "react"
import styles from "./Home.module.css"
import { Button, Typography } from "@mui/material";
import candSearchImg from "../../../public/assets/candidate.png"

const Home = () => {
    return ( 
        <div className={styles.container}>
            <div className={styles.title}>
                <Typography variant="h2">
                    Candidate Search Portal
                </Typography>
            </div>
            <div className={styles.description}>
                <Typography variant="h6">
                    Upload your JDs and get the best candidates for your job.
                </Typography>
            </div>
            <img src={candSearchImg}>
            </img>
            <div className={styles.buttondiv}>
                <Button href="/upload" variant="contained">
                    Upload Files
                </Button>
            </div>
            
        </div>
    );
}
export default Home;