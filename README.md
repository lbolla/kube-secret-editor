# Edit Kubernetes secrets

Usage:

    $> KUBE_EDITOR=/path/to/kube-secret-editor.py kubectl edit secret my-secret

The script will:
- decode the secret values coming from k8s
- call $EDITOR
- encode the values back

I have a handy shell alias to use it:

    alias kedit-secret="KUBE_EDITOR=kube-secret-editor kubectl edit secret"
