from unittest import TestCase
import tempfile, shutil, os
from listener import context

class ContextTests( TestCase ):
    def setUp( self ):
        self.workdir = tempfile.mkdtemp( 
            prefix='listener-', suffix='-test', dir='/dev/shm' 
        )
        self.context = context.Context(
            'default', directory=os.path.join(self.workdir,'config')
        )
    def tearDown( self ):
        shutil.rmtree( self.workdir, True ) # ignore errors
    
    def test_init( self ):
        pass 
    def test_language_model_directory( self ):
        assert os.path.exists( self.context.language_model_directory )
    def test_hmm_directory( self ):
        assert os.path.exists( self.context.hmm_directory )
    def test_buffer_directory( self ):
        assert os.path.exists( self.context.buffer_directory )
    def test_language_model_file( self ):
        assert os.path.exists( self.context.language_model_file )
    def test_dictionary_file( self ):
        assert os.path.exists( self.context.dictionary_file )
    
    def test_alsa_devices( self ):
        devices = self.context.available_alsa_devices()
        # obviously these *could* be false, but then you're running on a machine
        # that couldn't run the task...
        assert devices['input'], devices 
        assert devices['output'], devices

class AudioContextTests( TestCase ):
    def setUp( self ):
        self.workdir = tempfile.mkdtemp( prefix='listener-', suffix='-test' )
        self.context = context.Context('default', directory=self.workdir)
        self.audio_context = context.AudioContext( self.context, 'moo' )
    def tearDown( self ):
        shutil.rmtree( self.workdir, True ) # ignore errors
    def test_save_settings( self ):
        self.audio_context.save_settings()
        assert os.path.exists( self.audio_context.settings_file )
    def test_round_trip_settings( self ):
        base = self.audio_context.settings
        base['moo'] = 'this'
        self.audio_context.save_settings()
        assert os.path.exists( self.audio_context.settings_file )
        new_context = context.AudioContext( self.context, 'moo' )
        assert new_context.settings['moo'] == 'this'
    def test_transcription_filename( self ):
        filename = self.audio_context.transcription_filename( '  this/../:is a _+=| test ' )
        assert os.path.exists( filename )
        base = os.path.basename( filename )
        assert base.startswith( 'this_is_a_test-' ), base
        assert os.path.exists( self.audio_context.recording_directory )
        
