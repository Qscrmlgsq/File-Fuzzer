# File-Fuzzer
A Python class for fuzzing bytes of a file

How to use:

    with FileFuzzer(file) as ff:
    # Creates a FileFuzzer object, this also creates a backup of the file to allow it to be restored later.

        ff.fuzz_file(fuzz_percent=x, add_percent=y, remove_percent=z)
        # Fuzzes the bytes in a file.
        # fuzz_percent is the percentage chance that each byte will be replaced with a random byte.
        # add_percent is the percentage chance that a random byte will be added after each byte.
        # remove_percent is the percentage chance that each byte will be removed.
        # It is possible to use these together.
    
        ff.fuzz_file_exact_bytes(num_bytes)
        # Fuzzes exactly num_bytes bytes in the file, replacing them with a random byte.
        # The position of these bytes is chosen randomly.
  
    # Leaving the 'with' block removes the backup of the file and returns the file to it's original state
