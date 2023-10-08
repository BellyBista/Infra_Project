Creating and adding users to EKS:
1. Create a clusterrole and clussterrolebinding
    - reader
    - deploy,cm,pods,secrets,services = resources
    - verbs - get,list,watch
2. Go to aws IAM, create a role and policies to be attached to a group.
3. Create a group called developer and attache the role to the group.
4. Create a user called developer1 and add the user to the developer group.
5. Generate IAM credentials for the user (secret/access) = aws configure --profile developer1
- Update kubeconfig file => 
aws eks update-kubeconfig --region us-east-1 --name demo --profile developer1

6. Modify the aws-auth cm in the kube-system ns.
  mapUsers: |
      - userarn: arn:aws:iam::<>:user/developer1
        username: developer1
        groups:
         - reader

  kubectl auth can-i get *
