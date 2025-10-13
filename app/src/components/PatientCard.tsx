import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { User, Calendar, FileText, Heart } from "lucide-react";

interface PatientData {
  nome: string;
  idade: number;
  cpf: string;
  cartaoSUS: string;
  dataRegulacao: string;
  prioridade: "alta" | "media" | "baixa";
  especialidade: string;
  cid: string;
  descricaoCid: string;
  historicoClinico: string;
  medicacoes: string[];
  examesRealizados: string[];
  observacoes: string;
}

interface PatientCardProps {
  patient: PatientData;
}

export function PatientCard({ patient }: PatientCardProps) {
  const priorityColors = {
    alta: "rejected" as const,
    media: "pending" as const,
    baixa: "info" as const,
  };

  return (
    <Card className="p-6 space-y-6">
      <div className="flex items-start justify-between">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <User className="h-5 w-5 text-primary" />
            <h2 className="text-2xl font-bold text-foreground">{patient.nome}</h2>
          </div>
          <p className="text-sm text-muted-foreground">
            {patient.idade} anos • CNS: {patient.cartaoSUS}
          </p>
        </div>
        <Badge variant={priorityColors[patient.prioridade]} className="text-xs">
          Prioridade {patient.prioridade.toUpperCase()}
        </Badge>
      </div>

      <div className="grid grid-cols-2 gap-4 py-4 border-y border-border">
        <div className="space-y-1">
          <p className="text-xs text-muted-foreground">CPF</p>
          <p className="font-medium">{patient.cpf}</p>
        </div>
        <div className="space-y-1">
          <div className="flex items-center gap-1">
            <Calendar className="h-3 w-3 text-muted-foreground" />
            <p className="text-xs text-muted-foreground">Data de Regulação</p>
          </div>
          <p className="font-medium">{patient.dataRegulacao}</p>
        </div>
      </div>

      <div className="space-y-4">
        <div>
          <h3 className="text-sm font-semibold text-foreground mb-2 flex items-center gap-2">
            <FileText className="h-4 w-4 text-primary" />
            Dados Clínicos
          </h3>
          <div className="space-y-3 pl-6">
            <div>
              <p className="text-xs text-muted-foreground">Especialidade Solicitada</p>
              <p className="font-medium">{patient.especialidade}</p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground">CID-10</p>
              <p className="font-medium">
                {patient.cid} - {patient.descricaoCid}
              </p>
            </div>
          </div>
        </div>

        <div>
          <h3 className="text-sm font-semibold text-foreground mb-2 flex items-center gap-2">
            <Heart className="h-4 w-4 text-primary" />
            Histórico Clínico
          </h3>
          <p className="text-sm text-foreground pl-6">{patient.historicoClinico}</p>
        </div>

        {patient.medicacoes.length > 0 && (
          <div>
            <p className="text-sm font-semibold text-foreground mb-2">Medicações em Uso</p>
            <ul className="list-disc list-inside space-y-1 pl-6">
              {patient.medicacoes.map((med, idx) => (
                <li key={idx} className="text-sm text-foreground">
                  {med}
                </li>
              ))}
            </ul>
          </div>
        )}

        {patient.examesRealizados.length > 0 && (
          <div>
            <p className="text-sm font-semibold text-foreground mb-2">Exames Realizados</p>
            <ul className="list-disc list-inside space-y-1 pl-6">
              {patient.examesRealizados.map((exam, idx) => (
                <li key={idx} className="text-sm text-foreground">
                  {exam}
                </li>
              ))}
            </ul>
          </div>
        )}

        {patient.observacoes && (
          <div className="bg-muted/50 p-4 rounded-md">
            <p className="text-sm font-semibold text-foreground mb-1">Observações</p>
            <p className="text-sm text-foreground">{patient.observacoes}</p>
          </div>
        )}
      </div>
    </Card>
  );
}
