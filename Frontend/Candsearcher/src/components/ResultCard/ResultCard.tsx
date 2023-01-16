import { useState } from "react";
import * as React from 'react';
import styles from './ResultCard.module.css'
import { resultProps } from "../ResultsPage/types";
import { Button, Modal } from "@mui/material";
import { styled } from '@mui/material/styles';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
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


function BootstrapDialogTitle(props: DialogTitleProps) {
    const { children, onClose, ...other } = props;
  
    return (
      <DialogTitle sx={{ m: 0, p: 2 }} {...other}>
        {children}
        {onClose ? (
          <IconButton
            aria-label="close"
            onClick={onClose}
            sx={{
              color: (theme) => theme.palette.grey[500],
            }}
          >
            <CloseIcon />
          </IconButton>
        ) : null}
      </DialogTitle>
    );
  }

const Resultcard = (props : ResultCardprops ) => {


    const [open,setOpen] = useState<boolean>(false);

    const handleclick = ()=>{
        setOpen(true)
    }

    const handleClose = ()=>{
        setOpen(false)
    }

    let k : keyof typeof props.data

    return ( 
        <>
            <div className={styles.cardContainer}>
                <div className={styles.jobtitle}>
                    {props.data.name}
                </div>
                <div className={styles.location}>
                    {props.data.location}
                </div>
                <div className={styles.name}>
                    {props.data.education}
                </div>  
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
        <BootstrapDialogTitle id="customized-dialog-title" onClose={handleClose}>
          {props.data.jobTitle}
        </BootstrapDialogTitle>
        <DialogContent dividers>
        {
            Object.entries(props.data).map(([key,value]) => {
                return(
                    <>
                        <Typography gutterBottom>
                            {key.toUpperCase()}
                        </Typography>
                        <Typography gutterBottom>
                            {value.toLowerCase()}
                        </Typography>
                    </>
                )
            })
        }
        </DialogContent>
        <DialogActions>
          <Button autoFocus onClick={handleClose}>
            Ok!
          </Button>
        </DialogActions>
      </BootstrapDialog>
        </>
    );
}
 
export default Resultcard;