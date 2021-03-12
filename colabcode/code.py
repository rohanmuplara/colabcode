import os
import subprocess
# from pyngrok import ngrok

try:
    from google.colab import drive

    colab_env = True
except ImportError:
    colab_env = False


EXTENSIONS = ["ms-python.python", "jithurjacob.nbpreviewer"]


class ColabCode:
    def __init__(self, port=10000, password=None, mount_drive=False):
        self.port = port
        self.password = password
        self._mount = mount_drive
        self._install_code()
        self._install_extensions()
        self._start_server()
        self._run_code()

    def _install_code(self):
        subprocess.run(
            ["wget", "https://code-server.dev/install.sh"], stdout=subprocess.PIPE
        )
        subprocess.run(["sh", "install.sh"], stdout=subprocess.PIPE)

    def _install_extensions(self):
        for ext in EXTENSIONS:
            subprocess.run(["code-server", "--install-extension", f"{ext}"])

    def _start_server(self):
        # active_tunnels = ngrok.get_tunnels()
        # for tunnel in active_tunnels:
        #     public_url = tunnel.public_url
        #     ngrok.disconnect(public_url)
        # url = ngrok.connect(port=self.port, options={"bind_tls": True})
        # cm_0="chmod 400 ./tunnel_uplara"
        # cm_1 = "ssh -o StrictHostKeyChecking=no -i ./tunnel_uplara tmk@34.71.51.68 'sudo kill $(sudo lsof -t -i:3000)'"

        # try:
        #     out_0=subprocess.check_output(cm_0,stderr=subprocess.STDOUT,shell=True)
        #     out=subprocess.check_output(cm_1,stderr=subprocess.STDOUT,shell=True)
        # except subprocess.CalledProcessError as e:
        #     raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))

        # cm="chmod 400 /content/tunnel_uplara && ssh -o StrictHostKeyChecking=no -i /content/tunnel_uplara -N -R localhost:3000:localhost:3000 tmk@34.71.51.68"
        cm = "chmod 400 /content/tunnel_uplara && ssh -o StrictHostKeyChecking=no -i /content/tunnel_uplara -N -R localhost:{}:localhost:{} tmk@34.71.51.68".format(self.port, self.port)
        try:
            out=subprocess.Popen(cm,shell=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
        url = 'https://{}.colabcode.uplara.com'.format(self.port)
        print(f"fucker Code Server can be accessed on: {url}")

    def _run_code(self):
        os.system(f"fuser -n tcp -k {self.port}")
        if self._mount and colab_env:
            drive.mount("/content/drive")
        if self.password:
            code_cmd = f"PASSWORD={self.password} code-server --port {self.port} --disable-telemetry"
        else:
            code_cmd = f"code-server --port {self.port} --auth none --disable-telemetry"
        with subprocess.Popen(
            [code_cmd],
            shell=True,
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        ) as proc:
            for line in proc.stdout:
                print(line, end="")


# pip install git+https://github.com/uplara/colabcode.git
