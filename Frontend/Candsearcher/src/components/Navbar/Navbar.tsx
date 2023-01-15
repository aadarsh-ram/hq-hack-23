import { Button } from "@mui/material";
import * as React from "react"
import styles from "./Navbar.module.css"

const Navbar = () => {
    return ( 
        <div className={styles.navbar}>
            <div className={styles.navelement}>
                <Button href="/">
                    Home
                </Button>
            </div>
            <div className={styles.navelement}>
                <Button href="/upload">
                    Upload file
                </Button>
            </div>
            <div className={styles.navelement}>
                <Button href="/alluploads">
                    My uploads
                </Button>
            </div>
        </div>
    );
}
 
export default Navbar;