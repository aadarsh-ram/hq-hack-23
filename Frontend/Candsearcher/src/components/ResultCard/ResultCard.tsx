import { useState } from "react";
import * as React from 'react';
import styles from './ResultCard.module.css'
import { resultProps } from "../ResultsPage/types";
import { Button, Modal } from "@mui/material";
import { styled } from '@mui/material/styles';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import Typography from '@mui/material/Typography';

type ResultCardprops = {
    data : resultProps
}

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
    '& .MuiDialogContent-root': {
        padding: theme.spacing(2),
    },
    '& .MuiDialogActions-root': {
        padding: theme.spacing(1),
    },
}));

export interface DialogTitleProps {
    id: string;
    children?: React.ReactNode;
    onClose: () => void;
}

const Resultcard = (props : ResultCardprops ) => {


    const [open,setOpen] = useState<boolean>(false);

    const handleclick = ()=>{
        setOpen(true)
    }

    const handleClose = ()=>{
        setOpen(false)
    }

    return ( 
        <>
            <div className={styles.cardContainer}>
                <div className={styles.name}>
                    {props.data.name?.toLowerCase()}
                </div>
                <Typography variant="body1">
                    {props.data.location}
                </Typography>
                <Typography variant="body1">
                    {props.data.education}
                </Typography>  
                <div className={styles.showbutton}>
                    <Button onClick={handleclick}>
                        Show More
                    </Button>
                </div>
            </div>
            <BootstrapDialog
        onClose={handleClose}
        aria-labelledby="customized-dialog-title"
        open={open}
        className={styles.modal}
      >
        <DialogContent dividers>
        {
            Object.entries(props.data).map(([key,value]) => {
                return (
                    <div className={styles.modalContent}>
                        <Typography variant="h6" gutterBottom>
                            {key.toUpperCase()}
                        </Typography>
                        <Typography style={{whiteSpace: 'pre-line'}} gutterBottom>
                            {value === '' ? 'Not Available' : value}
                        </Typography>
                    </div>
                )
            })
        }
        </DialogContent>
        <DialogActions>
          <Button autoFocus onClick={handleClose}>
            Ok
          </Button>
        </DialogActions>
      </BootstrapDialog>
        </>
    );
}
 
export default Resultcard;