import errno
import os
import random
import shutil

class FileFuzzer(object):

    def __init__(self, file):
        self.file = file
        self._chunk_size = 8192 # hardcoded chunk size of 8KB


    def __enter__(self):
        """ Create a backup of the file we are going to fuzz"""
        self._backup = self.file + '.bkp'
        shutil.copyfile(self.file, self._backup) # copyfile will overwrite if _backup already exists
        return self


    def __exit__(self, type, value, traceback):
        """ Restore the file to it's original form from the backup"""
        self._safely_remove_file(self.file)
        os.rename(self._backup, self.file)


    def _safely_remove_file(self, file):
        if not os.path.isfile(self._backup):
            self._backup_file
        try:
            os.remove(file)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise


    def _coin_toss(self, percentage):
        # Do you feel lucky, punk?
        return random.uniform(0, 100) < percentage


    def _fuzz_chunk(self, chunk, fuzz_percent, add_percent, remove_percent):
        with open(self.file, 'ab') as f:
            for byte in chunk:
                if remove_percent > 0 and self._coin_toss(remove_percent):
                    pass
                else:
                    if fuzz_percent > 0 and self._coin_toss(fuzz_percent):
                        new_byte = chr(random.randint(0, 255))
                        f.write(new_byte)
                    else:
                        f.write(byte)
                if add_percent > 0 and self._coin_toss(add_percent):
                    add_byte = chr(random.randint(0, 255))
                    f.write(add_byte)


    def _fuzz_bytes(self, chunk, bytes_to_fuzz):
        with open(self.file, 'ab') as f:
            for i, byte in enumerate(chunk):
                if i in bytes_to_fuzz:
                    new_byte = chr(random.randint(0, 255))
                    f.write(new_byte)
                else:
                    f.write(byte)


    def fuzz_file(self, fuzz_percent = 0, add_percent = 0, remove_percent = 0):
        """ Fuzz a percentage of the bytes in a file randomly """
        # Remove previous version of file if it exists
        self._safely_remove_file(self.file)

        # Process each chunk of the file
        with open(self._backup, 'rb') as f:
            chunk = f.read(self._chunk_size)
            while chunk:
                self._fuzz_chunk(chunk, fuzz_percent, add_percent, remove_percent)
                chunk = f.read(self._chunk_size)


    def fuzz_file_exact_bytes(self, num_bytes):
        """ Fuzz an exact number of bytes in a file randomly """
        # Remove previous version of file if it exists
        self._safely_remove_file(self.file)

        file_size = int(os.path.getsize(self._backup))
        # We can't fuzz more bytes than are in our file
        num_bytes = min(file_size, num_bytes)

        bytes_to_fuzz = random.sample(xrange(file_size), num_bytes)
        bytes_to_fuzz.sort()
        # Process each chunk of the file
        with open(self._backup, 'rb') as f:
            chunk_count = 0
            chunk = f.read(self._chunk_size)
            while chunk:
                # get the position of all bytes to fuzz in the next chunk relative to the start of that chunk
                bytes_in_chunk_to_fuzz = [b % self._chunk_size for b in bytes_to_fuzz if b in xrange(chunk_count * self._chunk_size, (chunk_count + 1) * self._chunk_size)]
                self._fuzz_bytes(chunk, bytes_in_chunk_to_fuzz)
                chunk = f.read(self._chunk_size)
                chunk_count += 1