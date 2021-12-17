## IntCode updates:

### WaitingOnInput
Added the ability for the program to stop executing and wait for input through the use of WaitingOnInput Exception

### Halted
Because WaitingOnInput allows IntCode.run() to be called many times per program, added a Halted exception which will be thrown if run() is called after the program has ended

### next_output()
Gets the next output that hasn't been pulled from the queue of outputs yet. Wasn't strictly needed, but may be useful in the future and allows for more flexible output iteration

## Personal Thoughts:
I am LOVING this IntCode stuff!
