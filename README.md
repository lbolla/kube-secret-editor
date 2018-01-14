# Edit Kubernetes secrets

Usage:

    $> KUBE_EDITOR=/path/to/kube-secret-editor.py kubectl edit secret my-secret

The script will:
- decode the secret values coming from k8s
- call $EDITOR
- encode the values back
