# Project1 Repository Summer 2020 #

### This Project was part of Database models and Implementation Techniques coursework in UTA under Prof Ramirez Elmasari. ###

 #### Problem Statement ####
        ##### This project will implement a program that simulates the behavior of the two-phase locking (2PL) protocol for concurrency control.
              The particular protocol to be implemented will be rigorous 2PL, with the wound-wait method and wait die method(Extra credit) for dealing with     
              deadlock.
              The input to the program will be a file of transaction operations in a particular sequence.
              Each line has a single transaction operation.
              The possible operations are b (begin transaction), r (read item), w (write item), and e (end transaction).
              Each operation will be followed by a transaction id that is an integer between 1 and 9.
              For r and w operations, an item name follows between parentheses (item names are single letters from A to Z). #####
